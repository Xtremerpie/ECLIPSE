import tempfile,unittest
from pathlib import Path
from eclipse.engine import EclipseEngine
from eclipse.brain import SystemBrain
class BrainTests(unittest.TestCase):
 def test_read_only_and_unlocks(self):
  with tempfile.TemporaryDirectory() as d:
   e=EclipseEngine(Path(d)/'x.db',Path(d)/'none.json');b=SystemBrain(e);before=e.player()['xp'];r=b.snapshot();self.assertEqual(before,e.player()['xp']);self.assertTrue(r['chapters'][0]['unlocked']);self.assertFalse(r['achievements'][0]['unlocked']);q=e.quests()[0];e.complete_quest(q['id']);r=b.snapshot();self.assertTrue(r['achievements'][0]['unlocked']);self.assertTrue(r['chapters'][1]['unlocked']);e.close()
if __name__=='__main__':unittest.main()
