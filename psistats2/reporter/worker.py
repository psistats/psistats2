import threading
import time
import collections
import logging
import importlib
import traceback


def class_from_plugin_id(plugin_id):
  return ''.join([part.capitalize() for part in plugin_id.split('_')])


def load_plugins(plugin_configs, plugin_type):

  plugins = []

  for plugin_id, plugin_config in plugin_configs.items():

    if plugin_config['enabled'] is not True:
      continue

    if 'className' not in plugin_config:
      className = class_from_plugin_id(plugin_id)
      package = 'psistats2'
      module = 'plugins.' + plugin_type
    else:
      parts = plugin_config['className'].split('.')
      package = parts[0]
      if len(parts) > 2:
        module = parts[1:-1]
        className = parts[-1]
      else:
        module = ''
        className = parts[1]

    plugin_module = importlib.import_module('%s.%s' % (package, module))
    plugin_class = getattr(plugin_module, className)

    plugins.append(plugin_class(plugin_config['settings']))

  return plugins


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
    def __init__(self, hostname, config, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.config = config
      self.hostname = hostname
      self.logger = logging.getLogger(name='psireporter.manager')
      self.output_plugins = []
      self.reporter_plugins = []

      self.reporter_thread = None
      self.output_thread = None

      self.running = False

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
        self.logger.info('Loading plugins')

        self.output_plugins = load_plugins(self.config['outputters'], 'output')
        self.reporter_plugins = load_plugins(self.config['reporters'], 'reporters')

        for plugin in self.output_plugins:
          self.logger.debug('Plugin: %s:%s' % (plugin.PLUGIN_TYPE, plugin.PLUGIN_ID))

        for plugin in self.reporter_plugins:
          self.logger.debug('Plugin: %s:%s' % (plugin.PLUGIN_TYPE, plugin.PLUGIN_ID))

        o_manager = OutputManager(self.hostname, self.output_plugins, self.config)
        r_manager = ReporterManager(self.hostname, self.reporter_plugins, o_manager, self.config)

        o_manager.start()
        r_manager.start()

        while self.running is True:
          try:
            time.sleep(1)
          except KeyboardInterrupt:
            self.stop()

        o_manager.stop()
        r_manager.stop()
        o_manager.join()
        r_manager.join()

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
    def __init__(self, hostname, plugins, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(name='psireporter.output-manager')
        self._workers = []
        self.hostname = hostname
        self.config = config

        for plugin in plugins:
          plugin_id = plugin.PLUGIN_ID
          config = self.config['outputters'][plugin_id]

          if 'enabled' not in config:
            self.config['outputters'][plugin_id]['enabled'] = True

          if 'settings' not in config:
            self.config['outputters'][plugin_id]['settings'] = {}

          if self.config['outputters'][plugin_id]['enabled'] is not False:
            ow = OutputWorker(plugin)
            self._workers.append(ow)

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
            time.sleep(1)

        for worker in self._workers:
            worker.stop()

        while self.has_running_workers():
            time.sleep(1)

        self.logger.debug('Stopped')


class ReporterManager(threading.Thread):
    """Reporter Manager Thread

    Manages the various Reporter plugins and maintains the main loop
    of reporters."""
    def __init__(self, hostname, reporters, o_manager, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hostname = hostname
        self.config = config
        self.logger = logging.getLogger('psireporter.reporter-manager')

        self.running = False
        self._o_manager = o_manager

        self._reporter_counter = 0
        self._max_reporter_counter = 0

        self._reporters = {}
        self._outputters = {}
        self._triggers = {}
        self._counter = 1
        self._first_run = True

        for reporter in reporters:
          reporter_id = reporter.PLUGIN_ID
          config = self.config['reporters'][reporter.PLUGIN_ID]

          if 'interval' not in self.config['reporters'][reporter_id]:
              self.config['reporters'][reporter_id]['interval'] = 1

          if 'settings' not in self.config['reporters'][reporter_id]:
              self.config['reporters'][reporter_id]['settings'] = {}

          if 'enabled' not in self.config['reporters'][reporter_id]:
              self.config['reporters'][reporter_id]['enabled'] = False

          if self.config['reporters'][reporter_id]['enabled'] is not False:

              self._reporters[reporter_id] = reporter

              interval = self.config['reporters'][reporter_id]['interval']

              if interval not in self._triggers:
                  self._triggers[interval] = []

              self._triggers[interval].append(reporter_id)

        self._max_reporter_counter = max(self._triggers.keys())

        self._trigger_counters = self._triggers.keys()

    def start(self):
        """Start the Reporter Manager thread"""
        self.logger.debug('Starting...')
        self.running = True
        super().start()

    def stop(self):
        """Stops the Reporter Manager thread"""
        self.logger.debug('Stopping...')
        self.running = False

    def queue_report(self, reporter_id):
      reporter = self._reporters[reporter_id]
      report = reporter.report()

      message = {
          'hostname': self.hostname,
          'sender': reporter_id,
          'message': report
      }

      self._o_manager.add_report(message)




    def tick(self):
        """Executes every tick (1 second intervals)"""
        if self._counter > self._max_reporter_counter:
          self._counter = 1

        if self._first_run is True:
          for reporter_id in sorted(self._reporters.keys()):
            self.queue_report(reporter_id)

          self._first_run = False
        else:
          for counter in self._trigger_counters:
            if self._counter % counter == 0:
              for reporter_id in self._triggers[counter]:
                self.queue_report(reporter_id)

        self._counter += 1

    def run(self):
        """Starts the main loop"""
        self.logger.debug('Started')
        while self.running is True:
          try:
            self.tick()
          except Exception as e:
            self.logger.error(traceback.format_exc())
          time.sleep(1)

        self.logger.debug('Stopped')
