import tempfile, unittest
from pathlib import Path
from eclipse_v1.engine import EclipseEngine

class EngineV2Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.e=EclipseEngine(self.root/'test.db',self.root/'missing.json')
 def tearDown(self):self.e.close();self.tmp.cleanup()
 def test_daily_quests_and_one_time_reward(self):
  qs=self.e.quests();self.assertGreaterEqual(len(qs),5);q=qs[0];before=self.e.player()['xp'];self.assertTrue(self.e.complete_quest(q['id']));after=self.e.player()['xp'];self.assertEqual(after-before,q['xp']);self.assertFalse(self.e.complete_quest(q['id']));self.assertEqual(self.e.player()['xp'],after)
 def test_custom_quest_validation_and_completion(self):
  self.e.add_custom_quest('Build a small prototype','Creativity',35);q=next(q for q in self.e.quests() if q['title']=='Build a small prototype');self.assertEqual(q['xp'],35);self.assertTrue(self.e.complete_quest(q['id']));self.assertEqual(self.e.player()['attributes']['Creativity'],2)
  with self.assertRaises(ValueError):self.e.add_custom_quest('Bad','Unknown',10)
 def test_goal_rewards_and_delete(self):
  self.e.add_goal('Milestone');g=self.e.goals()[0];self.assertTrue(self.e.complete_goal(g['id']));self.assertFalse(self.e.complete_goal(g['id']));self.assertFalse(self.e.delete_goal(g['id']));self.e.add_goal('Remove me');self.assertTrue(self.e.delete_goal(self.e.goals()[0]['id']))
 def test_habit_checkin_once_per_day(self):
  self.e.add_habit('Read');h=self.e.habits()[0];before=self.e.player()['xp'];self.assertTrue(self.e.complete_habit(h['id']));self.assertFalse(self.e.complete_habit(h['id']));self.assertEqual(self.e.player()['xp']-before,10);self.assertEqual(self.e.habits()[0]['total_completions'],1)
 def test_reflection_persists(self):
  self.e.save_reflection('One thing I learned.');self.assertEqual(self.e.reflection(),'One thing I learned.')
 def test_export_import_round_trip(self):
  self.e.rename_player('Test Pilot');self.e.add_goal('Export test');self.e.add_habit('Walk');h=self.e.habits()[0];self.e.complete_habit(h['id']);out=self.root/'export.json';self.e.export_json(out);self.e.rename_player('Changed');self.e.import_json(out);self.assertEqual(self.e.player()['name'],'Test Pilot');self.assertEqual(len(self.e.goals()),1);self.assertEqual(len(self.e.habits()),1)
 def test_backup_is_valid_sqlite(self):
  out=self.root/'backup.db';self.e.backup(out);import sqlite3;c=sqlite3.connect(out);self.assertEqual(c.execute('PRAGMA integrity_check').fetchone()[0],'ok');c.close()
 def test_legacy_import_read_only(self):
  old=self.root/'eclipse_save.json';raw='{"name":"Legacy","xp":120,"coins":9,"stats":{"Focus":4}}';old.write_text(raw,encoding='utf8');self.e.close();self.e=EclipseEngine(self.root/'legacy.db',old);self.assertEqual(self.e.player()['name'],'Legacy');self.assertEqual(old.read_text(encoding='utf8'),raw)
 def test_v1_database_migration_is_read_only(self):
  old_path=self.root/'old.db';old=EclipseEngine(old_path,self.root/'no-old-save.json');old.rename_player('V1 Player');old.add_goal('Existing milestone');q=old.quests()[0];old.complete_quest(q['id']);old.close();before=old_path.read_bytes();new=EclipseEngine(self.root/'new.db',self.root/'missing.json',old_path);self.assertEqual(new.player()['name'],'V1 Player');self.assertGreaterEqual(new.player()['xp'],q['xp']);self.assertTrue(any(g['title']=='Existing milestone' for g in new.goals()));self.assertEqual(old_path.read_bytes(),before);new.close()
if __name__=='__main__':unittest.main()
