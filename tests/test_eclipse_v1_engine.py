import tempfile
import unittest
from pathlib import Path

from eclipse_v1.engine import EclipseEngine


class EclipseEngineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.engine = EclipseEngine(self.root / "test.db", self.root / "missing-legacy.json")

    def tearDown(self):
        self.engine.close()
        self.temp.cleanup()

    def test_daily_quests_are_created(self):
        quests = self.engine.quests()
        self.assertEqual(len(quests), 5)
        self.assertEqual(len({q["title"] for q in quests}), 5)

    def test_quest_rewards_only_once(self):
        quest = self.engine.quests()[0]
        before = self.engine.player()["xp"]
        self.assertTrue(self.engine.complete_quest(quest["id"]))
        after = self.engine.player()["xp"]
        self.assertEqual(after - before, quest["xp"])
        self.assertFalse(self.engine.complete_quest(quest["id"]))
        self.assertEqual(self.engine.player()["xp"], after)

    def test_goal_rewards_only_once(self):
        self.engine.add_goal("Finish a small project milestone")
        goal = self.engine.goals()[0]
        before = self.engine.player()["xp"]
        self.assertTrue(self.engine.complete_goal(goal["id"]))
        self.assertEqual(self.engine.player()["xp"] - before, 30)
        self.assertFalse(self.engine.complete_goal(goal["id"]))

    def test_legacy_import_is_read_only(self):
        legacy = self.root / "eclipse_save.json"
        original = '{"name":"Legacy Player","xp":145,"coins":12,"stats":{"Focus":4}}'
        legacy.write_text(original, encoding="utf-8")
        self.engine.close()
        self.engine = EclipseEngine(self.root / "legacy.db", legacy)
        profile = self.engine.player()
        self.assertEqual(profile["name"], "Legacy Player")
        self.assertEqual(profile["xp"], 145)
        self.assertEqual(profile["attributes"]["Focus"], 4)
        self.assertEqual(legacy.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
