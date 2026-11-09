import tempfile
import unittest
from pathlib import Path

from eclipse.engine import EclipseEngine
from eclipse.brain import SystemBrain


class SystemBrainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.engine = EclipseEngine(self.root / "brain.db", self.root / "missing.json")
        self.brain = SystemBrain(self.engine)

    def tearDown(self):
        self.engine.close()
        self.temp.cleanup()

    def test_initial_recommendation_does_not_invent_history(self):
        report = self.brain.snapshot()
        self.assertEqual(report["quest_records"], 0)
        self.assertEqual(report["goal_records"], 0)
        self.assertFalse(report["achievements"][0]["unlocked"])
        self.assertTrue(report["chapters"][0]["unlocked"])
        self.assertFalse(report["chapters"][1]["unlocked"])

    def test_quest_record_unlocks_milestones_and_story(self):
        quest = self.engine.quests()[0]
        self.assertTrue(self.engine.complete_quest(quest["id"]))
        report = self.brain.snapshot()
        self.assertEqual(report["quest_records"], 1)
        self.assertTrue(report["achievements"][0]["unlocked"])
        self.assertTrue(report["chapters"][1]["unlocked"])

    def test_brain_is_read_only(self):
        before = self.engine.player()["xp"]
        self.brain.snapshot()
        self.assertEqual(self.engine.player()["xp"], before)


if __name__ == "__main__":
    unittest.main()
