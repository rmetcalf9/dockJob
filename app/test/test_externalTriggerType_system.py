import unittest
import pytest
from ExternalTriggers import getAllTriggerTypeInstances

@pytest.mark.externalTriggerSystemTest
class test_jobExecutionsData(unittest.TestCase):

  def test_all_types_setup(self):
    instances = getAllTriggerTypeInstances()
    self.assertEqual(list(instances.keys()), ["googleDriveRawClass", "googleDriveNewFileWatchClass"])
