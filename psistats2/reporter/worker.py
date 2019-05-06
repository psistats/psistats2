import threading
import time
import collections
import logging
from datetime import datetime
import uuid
import calendar
from psistats2.reporter.registry import Registry


class Report(tuple):
    """Report

    This class wraps the data returned by reporters before it is
    sent to an output plugin"""
    __slots__ = []

    def __new__(cls, **kwargs):
        return tuple.__new__(cls, (
            kwargs.get('id', str(uuid.uuid1())),
            kwargs.get('message', None),
            kwargs.get('sender', None),
            calendar.timegm(datetime.utcnow().utctimetuple())
        ))

    @property
    def id(self):
        """Report ID"""
        return tuple.__getitem__(self, 0)

    @property
    def message(self):
        """Report Message

        This can be any kind of value"""
        return tuple.__getitem__(self, 1)

    @property
    def timestamp(self):
        """Timestamp in seconds when the report was genreated"""
        return tuple.__getitem__(self, 3)

    @property
    def sender(self):
        """Which reporter plugin sent this report"""
        return tuple.__getitem__(self, 2)

    def __iter__(self):
        for key in ['id', 'timestamp', 'message', 'sender']:
            yield (key, getattr(self, key))


class Manager(threading.Thread):
    """Manager Thread

    This is the main manager for psireporter. It will handle all work
    of calling reporters at their required intervals, generating
    Report objects, and sending them to the output plugins.

    The configuration should look something like this::

        {
        'reporters': {
            'reporter-id': {
              'interval': 1,
              'enabled': True,
              'settings': {}
            }
        },
        'outputters': {
            'output-id': {
               'enabled': False,
               'settings': {}
          }
        }

    'reporters' is a list of reporter plugin configurations. Each
    configuration has 'interval', 'enabled', and 'settings'.

    'outputters' is a list of output plugin configurations. Each
    configuration has 'enabled', and 'settings'.

    The 'settings' dict is given to a plugin via the 'config'
    attribute. This attribute is only available after construction
    thus it is not available the plugin's __init__() method.

    :param config: object Configuration object
    :param reportClass: Report Which report class to use
    """
    def __init__(self, config=None, reportClass=Report, *args, **kwargs):

        self.logger = logging.getLogger(name='psireporter.manager')

        self.running = False

        if config is None:
            self.config = {}
        else:
            self.config = config

        self._reportClass = reportClass

        super().__init__(*args, **kwargs)

    def start(self):
        """Start the Manager thread"""
        self.logger.debug('Starting...')
        self.running = True
        super().start()

    def stop(self):
        """Stop the manager thread"""
        self.logger.debug('Stopping...')
        self.running = False

    def run(self):
        """Starts the main loop"""
        self.logger.debug('Start manager threads')
        outputters = Registry.GetEntries('outputters')
        reporters = Registry.GetEntries('reporters')

        print('total outputters: %s' % len(outputters))
        print('total reporters: %s' % len(reporters))

        o_manager = OutputManager(outputters, self.config.get('outputters', {}))
        r_manager = ReporterManager(reporters, o_manager, self.config.get('reporters', {}),
            reportClass=self._reportClass
        )

        o_manager.start()
        r_manager.start()

        self.logger.debug('Started')
        while self.running is True:
            time.sleep(5)

        o_manager.stop()
        r_manager.stop()

        self.logger.debug('Stopped')


class OutputWorker(threading.Thread):
    """A thread that manages sending reports to an output plugin

    It maintains its own queue separate from the main report queue, ensuring that
    if errors or slowness occurs, no reports are lost."""
    def __init__(self, outputter, *args, **kwargs):

        logName = 'psireporter.output-worker' + outputter.__class__.__name__

        self.logger = logging.getLogger(name=logName)
        self.report_queue = collections.deque()
        self.running = False
        self.outputter = outputter
        super().__init__(*args, **kwargs)

    def start(self):
        """Start the Output Worker thread"""
        self.running = True
        self.logger.debug('Starting...')
        super().start()

    def stop(self):
        """Stop the Output Worker thread"""
        self.logger.debug('Stopping...')
        self.running = False

    def add_report(self, report):
        """Add report to the output queue"""
        self.report_queue.append(report)

    def tick(self):
        """Executes every loop"""
        if len(self.report_queue) > 0:
            report = self.report_queue.popleft()
            self.outputter.send(report)
        else:
            time.sleep(1)

    def run(self):
        """Stars the main loop"""
        self.logger.debug('Started')

        while self.running is True:
            self.tick()

        self.logger.debug('Stopped')


class OutputManager(threading.Thread):
    """Output Manager Thread

    Manages output plugins and a master queue of reports."""
    def __init__(self, outputters, config=None, *args, **kwargs):
        self.logger = logging.getLogger(name='psireporter.output-manager')
        self._workers = []

        if config is None:
            self.config = {}
        else:
            self.config = config

        for outputter_id, outputter in outputters:

            if outputter_id not in self.config:
                self.config[outputter_id] = {
                    'enabled': True,
                    'settings': {}
                }
            else:
                if 'enabled' not in self.config[outputter_id]:
                    self.config[outputter_id]['enabled'] = True

                if 'settings' not in self.config[outputter_id]:
                    self.config[outputter_id]['settings'] = {}

            if self.config[outputter_id]['enabled'] is not False:

                print('OUTPUTTER:', outputter)

                plugin = outputter(self.config[outputter_id]['settings'])
                ow = OutputWorker(plugin)

                self._workers.append(ow)

        super().__init__(*args, **kwargs)

    def start(self):
        """Starts the Output Manager thread"""
        self.logger.debug('Starting...')
        self.running = True
        super().start()

    def stop(self):
        """Stops the Output Manager thread"""
        self.logger.debug('Stopping...')
        self.running = False

    def add_report(self, report):
        """Add a report to the master queue"""
        for worker in self._workers:
            worker.add_report(report)

    def has_running_workers(self):
        """Returns True if there are running OutputWorker threads"""
        for worker in self._workers:
            if worker.running is True:
                return True
        return False

    def run(self):
        """Starts the main loop"""
        for worker in self._workers:
            worker.start()

        self.logger.debug('Started')

        while self.running is True:
            time.sleep(10)

        for worker in self._workers:
            worker.stop()

        while self.has_running_workers():
            time.sleep(10)

        self.logger.debug('Stopped')


class ReporterManager(threading.Thread):
    """Reporter Manager Thread

    Manages the various Reporter plugins and maintains the main loop
    of reporters."""
    def __init__(self, reporters, o_manager, config=None, *args, **kwargs):

        self.logger = logging.getLogger('psireporter.reporter-manager')

        if config is None:
            self.config = {}
        else:
            self.config = config

        self.running = False
        self._o_manager = o_manager

        self._reporter_counter = 0
        self._max_reporter_counter = 0

        self._reportClass = kwargs.get('reportClass', Report)

        if 'reportClass' in kwargs:
            del kwargs['reportClass']

        self._reporters = {}
        self._outputters = {}
        self._triggers = {}
        self._counter = 1
        self._first_run = True

        for reporter_id, reporter in reporters:

            if reporter_id not in self.config:
                self.config[reporter_id] = {
                    'interval': 1,
                    'enabled': True,
                    'settings': {}
                }
            else:
                if 'interval' not in self.config[reporter_id]:
                    self.config[reporter_id]['interval'] = 1

                if 'settings' not in self.config[reporter_id]:
                    self.config[reporter_id]['settings'] = {}

                if 'enabled' not in self.config[reporter_id]:
                    self.config[reporter_id]['enabled'] = True

            if self.config[reporter_id]['enabled'] is not False:

                self._reporters[reporter_id] = reporter(self.config[reporter_id]['settings'])

                interval = self.config[reporter_id]['interval']

                if interval not in self._triggers:
                    self._triggers[interval] = []

                self._triggers[interval].append(reporter_id)

        self._max_reporter_counter = max(self._triggers.keys())

        self._trigger_counters = self._triggers.keys()

        super().__init__(*args, **kwargs)

    def start(self):
        """Start the Reporter Manager thread"""
        self.logger.debug('Starting...')
        self.running = True
        super().start()

    def stop(self):
        """Stops the Reporter Manager thread"""
        self.logger.debug('Stopping...')
        self.running = False

    def tick(self):
        """Executes every tick (1 second intervals)"""
        if self._counter > self._max_reporter_counter:
            self._counter = 1

        if self._first_run is True:
            for reporter_id in sorted(self._reporters.keys()):
                reporter = self._reporters[reporter_id]
                message = reporter.report()

                report = self._reportClass(message=message, sender=reporter_id)

                self._o_manager.add_report(report)
            self._first_run = False
        else:
            for counter in self._trigger_counters:
                if self._counter % counter == 0:
                    for reporter_id in self._triggers[counter]:
                        reporter = self._reporters[reporter_id]
                        message = reporter.report()

                        report = self._reportClass(message=message, sender=reporter_id)

                        self._o_manager.add_report(report)
        self._counter += 1

    def run(self):
        """Starts the main loop"""
        self.logger.debug('Started')
        while self.running is True:
            self.tick()
            time.sleep(1)

        self.logger.debug('Stopped')
