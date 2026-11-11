import tempfile,unittest
from pathlib import Path
from eclipse.engine import EclipseEngine
from eclipse.brain import SystemBrain
class BrainTests(unittest.TestCase):
 def test_analysis_preferences_are_respected(self):
  with tempfile.TemporaryDirectory() as d:
   e=EclipseEngine(Path(d)/'x.db',Path(d)/'none.json');b=SystemBrain(e)
   e.save_daily_checkin(mood=5,energy=5,focus=5,win='A win')
   report=b.daily_report(7,True,True,False,False)
   self.assertIn('Daily pulse analysis is disabled',report)
   self.assertNotIn("TODAY'S SELF-REPORTED PULSE",report)
   self.assertIn('Objectives completed       0',report)
   e.close()
 def test_read_only_and_unlocks(self):
  with tempfile.TemporaryDirectory() as d:
   e=EclipseEngine(Path(d)/'x.db',Path(d)/'none.json');b=SystemBrain(e);before=e.player()['xp'];r=b.snapshot();self.assertEqual(before,e.player()['xp']);self.assertTrue(r['chapters'][0]['unlocked']);self.assertFalse(r['achievements'][0]['unlocked']);q=e.quests()[0];e.complete_quest(q['id']);r=b.snapshot();self.assertTrue(r['achievements'][0]['unlocked']);self.assertTrue(r['chapters'][1]['unlocked']);e.close()
if __name__=='__main__':unittest.main()
