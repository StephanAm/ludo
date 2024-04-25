from ludocommon import GameStatus,GameConfig,buildRequired
from datetime import datetime
import json
import unittest

class GameStatusTests(unittest.TestCase):
    @property
    def status(self): return GameStatus(
        importSource='some/source',
        importConfigHash="",
        importTimeStamp="2024-04-19 20:13:16",
        buildTimeStamp="2024-04-19 20:13:17",
        buildNumber="",
        buildConfigHash="hash",
        wrapTimeStamp="2024-04-19 20:13:16",
        wrapConfigHash=""
    )
    @property
    def config(self): return GameConfig(
        name = "game name",
        fullname = "Full Game Name",
        wrapper = "dosbox",
        runcommand = "run",
        source = "some/source",
        version = "0.0.0"
    )
    
    def test_buildRequired_returnsFalseWhenTimestampsAndHashMatches(self):
        status = self.status
        config = self.config
        status.buildConfigHash = config.getHash()
        res = buildRequired(config,status)
        self.assertFalse(res)

    def test_buildRequired_returnsTrueWhenImportOutOfDate(self):
            status = self.status
            config = self.config
            status.configHash = config.getHash()
            status.importTimeStamp="2024-04-19 20:13:17"
            status.buildTimeStamp="2024-04-19 20:13:16"
                
            res = buildRequired(config,status)
            self.assertTrue(res)

    def test_buildRequired_returnsTrueWhenLastBuildNotSet(self):
        status = self.status
        config = self.config
        status.configHash = config.getHash()
        status.buildTimeStamp = ''
        res = buildRequired(config,status)
        self.assertTrue(res)
    
    def test_buildRequired_returnsTrueWhenConfigChanges(self):
        status = self.status
        config = self.config
        status.buildConfigHash = config.getHash()
        res = buildRequired(config,status)
        self.assertFalse(res)
        config.name = 'some other name'
        res2 = buildRequired(config,status)
        self.assertTrue(res2)

    def test_configGetHash_HashesMapForDifferentInstances(self):
         c1 = self.config
         c2 = self.config
         h1 = c1.getHash()
         h2 = c2.getHash()
         self.assertFalse(c1 is c2)
         self.assertEqual(h1,h2)