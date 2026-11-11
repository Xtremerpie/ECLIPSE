import tempfile, unittest
from datetime import date
from pathlib import Path
from eclipse.engine import EclipseEngine

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

 def test_daily_pulse_and_settings_persist(self):
  self.e.save_daily_checkin(mood=4,energy=3,focus=5,win='Finished a task',challenge='Distraction',priority='Study')
  pulse=self.e.daily_checkin()
  self.assertEqual(pulse['mood'],4);self.assertEqual(pulse['priority'],'Study')
  self.e.set_setting('analysis_window','14')
  self.assertEqual(self.e.get_setting('analysis_window'),'14')
 def test_focus_session_and_analytics(self):
  self.e.record_focus_session(25,True);self.e.log_session('app_opened','Test session')
  data=self.e.analytics_snapshot(7)
  self.assertEqual(data['focus_minutes'],25);self.assertGreaterEqual(data['session_count'],1)
 def test_period_comparison_and_daily_timeline(self):
  from datetime import date,timedelta
  q=self.e.quests()[0];self.e.complete_quest(q['id'])
  snap=self.e.analytics_snapshot(7)
  self.assertEqual(snap['quest_count'],1);self.assertEqual(snap['previous_quest_count'],0)
  timeline=self.e.activity_by_day(7)
  self.assertEqual(len(timeline),7);self.assertEqual(sum(x['quests'] for x in timeline),1)
 def test_daily_prompt_setting_persists(self):
  self.e.set_setting('last_checkin_prompt_date',date.today().isoformat())
  self.assertEqual(self.e.get_setting('last_checkin_prompt_date'),date.today().isoformat())
  self.e.set_setting('include_checkins','0')
  self.assertEqual(self.e.get_setting('include_checkins'),'0')
 def test_v2_export_import_compatibility(self):
  import json
  out=self.root/'v2.json';tables={}
  for table in ('player','attributes','quests','events','goals','habits','habit_logs','reflections'):
   tables[table]=[dict(row) for row in self.e.conn.execute('SELECT * FROM '+table)]
  out.write_text(json.dumps({'app':'ECLIPSE','format_version':2,'tables':tables}),encoding='utf8')
  self.e.rename_player('After V2');self.e.import_json(out)
  self.assertEqual(self.e.player()['name'],'Player')

if __name__=='__main__':unittest.main()
