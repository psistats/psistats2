from psistats2.reporter import PsistatsReporterPlugin
from psistats2.reporter import PsistatsOutputPlugin
from psistats2.reporter import PsistatsPlugin
import pytest


def test_broken_reporter_plugin():

  class TestReporter(PsistatsReporterPlugin):
    pass

  with pytest.raises(RuntimeError):
    TestReporter({})


def test_reporter_plugin():

  class TestReporter(PsistatsReporterPlugin):
    PLUGIN_ID = 'test-reporter'

  tr = TestReporter({
      'foo': 'bar'
  })

  assert tr.config['foo'] == 'bar'
  assert tr.PLUGIN_TYPE == 'reporter'


def test_broken_plugin_type():
  class TestPlugin(PsistatsPlugin):
    PLUGIN_ID = 'broken-plugin'

  with pytest.raises(RuntimeError):
    TestPlugin({})


def test_broken_output_plugin():
  class TestOutputPlugin(PsistatsOutputPlugin):
    pass

  with pytest.raises(RuntimeError):
    TestOutputPlugin({})


def test_output_plugin():
  class TestOutputPlugin(PsistatsOutputPlugin):
    PLUGIN_ID = 'output-plugin'

  to = TestOutputPlugin({'foo': 'bar'})

  assert to.PLUGIN_TYPE == 'output'
  assert to.config['foo'] == 'bar'
