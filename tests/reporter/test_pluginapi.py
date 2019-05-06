from psistats2.reporter.registry import Registry
from psistats2.reporter import ReporterPlugin
from psistats2.reporter import OutputPlugin
import pytest


@pytest.yield_fixture(autouse=True)
def setup_registry():
    Registry.ClearAll()


def test_reporter_plugin():

    class TestReporter(metaclass=ReporterPlugin):
        pass

    class IdTestReporter(metaclass=ReporterPlugin):
        PLUGIN_ID = 'test-id'

    assert Registry.HasEntry('reporters', 'test-id') is True

    nonIdReporter = [reporter for reporter in Registry.GetEntries('reporters') if reporter[0].endswith('TestReporter')]
    assert len(nonIdReporter) is 1


def test_outputer_plugin():

    class TestOutputter(metaclass=OutputPlugin):
        pass

    class IdTestOutputter(metaclass=OutputPlugin):
        PLUGIN_ID = 'outputter-id'

    assert Registry.HasEntry('outputters', 'outputter-id') is True

    nonIdOutputter = [o for o in Registry.GetEntries('outputters') if o[0].endswith('TestOutputter')]
    assert len(nonIdOutputter) is 1

def test_outputter_config():

    class TestOutputter(metaclass=OutputPlugin):
        pass

    to = TestOutputter()

    assert to.config == {}


def test_reporter_config():

    class TestReporter(metaclass=ReporterPlugin):
        pass

    tr = TestReporter()

    assert tr.config == {}
