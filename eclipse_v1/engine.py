"""ECLIPSE 2.0 local progression engine. No network access or device monitoring."""
from __future__ import annotations
import json, random, sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

RANKS = [(1,"F"),(5,"E"),(10,"D"),(20,"C"),(35,"B"),(55,"A"),(80,"S"),(120,"SS")]
ATTRIBUTES = ("Knowledge","Focus","Discipline","Creativity","Courage","Social","Resilience","Awareness")
QUEST_POOL = [
 ("Knowledge","Study one topic with full attention",20),
 ("Focus","Complete one focused work session",20),
 ("Discipline","Organise one small part of your workspace",15),
 ("Creativity","Build, sketch, or improve something",25),
 ("Courage","Take one reasonable step you've been postponing",20),
 ("Social","Have one meaningful, respectful conversation",15),
 ("Resilience","Return to a task after a setback",20),
 ("Awareness","Reflect on what worked today",15),
]
STORY = [
 ("PROLOGUE · THE UNKNOWN","A quiet signal appears in the noise. It does not command you. It offers a question: what will you choose to become?"),
 ("CHAPTER 01 · FIRST SYNCHRONIZATION","The System learns your chosen goals. Every record is a fragment of a larger map. Nothing is unlocked by pretending; the world responds to real effort."),
 ("CHAPTER 02 · THE AWAKENING","The first milestone is not power. It is awareness: seeing your actions clearly and choosing the next useful step."),
 ("CHAPTER 03 · THE ARCHIVE","Across the hidden archive, small completed promises become a pattern. The origin of the signal remains unknown."),
 ("CHAPTER 04 · THE BUILDER","A pattern becomes a direction. The System records not perfection, but the ability to return and continue."),
]

class EclipseEngine:
 def __init__(self, db_path="eclipse_v1.db", legacy_path="eclipse_save.json", migration_path=None):
  self.db_path=Path(db_path); self.db_path.parent.mkdir(parents=True,exist_ok=True)
  self.conn=sqlite3.connect(self.db_path); self.conn.row_factory=sqlite3.Row
  self.conn.execute("PRAGMA foreign_keys=ON"); self._schema(); self._seed(); self._import_legacy(Path(legacy_path))
  if migration_path: self._migrate_v1_database(Path(migration_path))
 def _schema(self):
  self.conn.executescript("""
  CREATE TABLE IF NOT EXISTS player(id INTEGER PRIMARY KEY CHECK(id=1),name TEXT NOT NULL DEFAULT 'Player',xp INTEGER NOT NULL DEFAULT 0,coins INTEGER NOT NULL DEFAULT 0,created_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS attributes(name TEXT PRIMARY KEY,value INTEGER NOT NULL DEFAULT 1);
  CREATE TABLE IF NOT EXISTS quests(id INTEGER PRIMARY KEY AUTOINCREMENT,day TEXT NOT NULL,title TEXT NOT NULL,category TEXT NOT NULL,xp INTEGER NOT NULL,completed INTEGER NOT NULL DEFAULT 0,completed_at TEXT,UNIQUE(day,title));
  CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,kind TEXT NOT NULL,detail TEXT NOT NULL,created_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS goals(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,completed INTEGER NOT NULL DEFAULT 0,created_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS habits(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,created_at TEXT NOT NULL,active INTEGER NOT NULL DEFAULT 1);
  CREATE TABLE IF NOT EXISTS habit_logs(id INTEGER PRIMARY KEY AUTOINCREMENT,habit_id INTEGER NOT NULL,day TEXT NOT NULL,completed_at TEXT NOT NULL,UNIQUE(habit_id,day),FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE);
  CREATE TABLE IF NOT EXISTS reflections(day TEXT PRIMARY KEY,note TEXT NOT NULL,updated_at TEXT NOT NULL);
  """); self.conn.commit()
 def _seed(self):
  self.conn.execute("INSERT OR IGNORE INTO player(id,name,created_at) VALUES(1,'Player',?)",(datetime.now().isoformat(timespec='seconds'),))
  for a in ATTRIBUTES:self.conn.execute("INSERT OR IGNORE INTO attributes(name,value) VALUES(?,1)",(a,))
  self.conn.commit(); self.ensure_daily_quests()
 def _event(self,k,d): self.conn.execute("INSERT INTO events(kind,detail,created_at) VALUES(?,?,?)",(k,d,datetime.now().isoformat(timespec='seconds')))
 def _import_legacy(self,path):
  if self.conn.execute("SELECT 1 FROM events WHERE kind='legacy_import' LIMIT 1").fetchone() or not path.exists():return
  try:
   data=json.loads(path.read_text(encoding='utf-8')); self.conn.execute("UPDATE player SET name=?,xp=?,coins=? WHERE id=1",(str(data.get('name','Player'))[:40],max(0,int(data.get('xp',0))),max(0,int(data.get('coins',0)))))
   for k,v in data.get('stats',{}).items():
    if k in ATTRIBUTES:self.conn.execute("UPDATE attributes SET value=? WHERE name=?",(max(1,min(999,int(v))),k))
   self._event('legacy_import','Imported compatible profile from eclipse_save.json'); self.conn.commit()
  except (OSError,ValueError,TypeError,json.JSONDecodeError): self._event('legacy_import_skipped','Legacy save could not be safely imported'); self.conn.commit()
 def _migrate_v1_database(self,source):
  """Copy compatible V1 records without modifying the original database."""
  if not source.exists() or source.resolve()==self.db_path.resolve():return
  if self.conn.execute("SELECT 1 FROM events WHERE kind='v1_database_import' LIMIT 1").fetchone():return
  try:
   old=sqlite3.connect(f"file:{source.resolve().as_posix()}?mode=ro",uri=True);old.row_factory=sqlite3.Row
   tables={r[0] for r in old.execute("SELECT name FROM sqlite_master WHERE type='table'")}
   if not {'player','attributes','events','goals'}.issubset(tables):old.close();return
   player=old.execute('SELECT * FROM player WHERE id=1').fetchone()
   with self.conn:
    if player:self.conn.execute('UPDATE player SET name=?,xp=MAX(xp,?),coins=MAX(coins,?) WHERE id=1',(str(player['name'])[:40],max(0,int(player['xp'])),max(0,int(player['coins']))))
    for row in old.execute('SELECT name,value FROM attributes'):
     if row['name'] in ATTRIBUTES:self.conn.execute('UPDATE attributes SET value=MAX(value,?) WHERE name=?',(max(1,min(999,int(row['value']))),row['name']))
    for row in old.execute('SELECT title,completed,created_at FROM goals'):
     if not self.conn.execute('SELECT 1 FROM goals WHERE title=? AND created_at=?',(row['title'],row['created_at'])).fetchone():self.conn.execute('INSERT INTO goals(title,completed,created_at) VALUES(?,?,?)',(row['title'],row['completed'],row['created_at']))
    for row in old.execute('SELECT kind,detail,created_at FROM events'):
     if not self.conn.execute('SELECT 1 FROM events WHERE kind=? AND detail=? AND created_at=?',(row['kind'],row['detail'],row['created_at'])).fetchone():self.conn.execute('INSERT INTO events(kind,detail,created_at) VALUES(?,?,?)',(row['kind'],row['detail'],row['created_at']))
    if 'quests' in tables:
     for row in old.execute('SELECT day,title,category,xp,completed,completed_at FROM quests'):self.conn.execute('INSERT OR IGNORE INTO quests(day,title,category,xp,completed,completed_at) VALUES(?,?,?,?,?,?)',(row['day'],row['title'],row['category'],row['xp'],row['completed'],row['completed_at']))
    self._event('v1_database_import',f'Imported compatible progress from {source.name}; original file left unchanged')
   old.close()
  except (sqlite3.Error,KeyError,ValueError,TypeError):
   try:old.close()
   except Exception:pass
   self._event('v1_database_import_skipped','Previous V1 database could not be safely imported');self.conn.commit()
 def ensure_daily_quests(self):
  today=date.today().isoformat()
  if self.conn.execute("SELECT COUNT(*) FROM quests WHERE day=?",(today,)).fetchone()[0]:return
  rng=random.Random(today)
  for cat,title,xp in rng.sample(QUEST_POOL,5):self.conn.execute("INSERT OR IGNORE INTO quests(day,title,category,xp) VALUES(?,?,?,?)",(today,title,cat,xp))
  self.conn.commit()
 def player(self):
  p=dict(self.conn.execute('SELECT * FROM player WHERE id=1').fetchone());lvl=1;rem=p['xp']
  while rem>=lvl*100:rem-=lvl*100;lvl+=1
  rank='F'
  for threshold,label in RANKS:
   if lvl>=threshold:rank=label
  p.update(level=lvl,level_xp=rem,next_xp=lvl*100,rank=rank,attributes={r['name']:r['value'] for r in self.conn.execute('SELECT * FROM attributes ORDER BY name')});return p
 def rename_player(self,name):
  name=name.strip()[:40]
  if not name:raise ValueError('Player name cannot be empty')
  self.conn.execute('UPDATE player SET name=? WHERE id=1',(name,));self._event('profile_updated',f'Player name changed to {name}');self.conn.commit()
 def quests(self,all_days=False):
  self.ensure_daily_quests();sql='SELECT * FROM quests ORDER BY day DESC,id DESC' if all_days else 'SELECT * FROM quests WHERE day=? ORDER BY id'
  rows=self.conn.execute(sql,() if all_days else (date.today().isoformat(),));return [dict(x) for x in rows]
 def add_custom_quest(self,title,category,xp=20):
  title=title.strip()[:120]
  if not title:raise ValueError('Quest title cannot be empty')
  if category not in ATTRIBUTES:raise ValueError('Unknown attribute')
  xp=max(5,min(50,int(xp)));self.conn.execute('INSERT INTO quests(day,title,category,xp) VALUES(?,?,?,?)',(date.today().isoformat(),title,category,xp));self._event('quest_created',f'Custom quest added: {title}');self.conn.commit()
 def delete_quest(self,qid):
  cur=self.conn.execute('DELETE FROM quests WHERE id=? AND day=? AND completed=0',(qid,date.today().isoformat()))
  if cur.rowcount:self._event('quest_removed',f'Uncompleted quest #{qid} removed');self.conn.commit();return True
  return False
 def complete_quest(self,qid):
  row=self.conn.execute('SELECT * FROM quests WHERE id=? AND day=?',(qid,date.today().isoformat())).fetchone()
  if not row or row['completed']:return False
  self.conn.execute('UPDATE quests SET completed=1,completed_at=? WHERE id=?',(datetime.now().isoformat(timespec='seconds'),qid));self.conn.execute('UPDATE player SET xp=xp+?,coins=coins+5 WHERE id=1',(row['xp'],));self.conn.execute('UPDATE attributes SET value=MIN(999,value+1) WHERE name=?',(row['category'],));self._event('quest_completed',f"{row['title']} (+{row['xp']} XP)");self.conn.commit();return True
 def add_goal(self,title):
  title=title.strip()[:120]
  if not title:raise ValueError('Objective cannot be empty')
  self.conn.execute('INSERT INTO goals(title,created_at) VALUES(?,?)',(title,datetime.now().isoformat(timespec='seconds')));self._event('goal_created',f'Objective added: {title}');self.conn.commit()
 def goals(self):return [dict(r) for r in self.conn.execute('SELECT * FROM goals ORDER BY id DESC')]
 def complete_goal(self,gid):
  cur=self.conn.execute('UPDATE goals SET completed=1 WHERE id=? AND completed=0',(gid,))
  if cur.rowcount:self.conn.execute('UPDATE player SET xp=xp+30,coins=coins+10 WHERE id=1');self._event('goal_completed',f'Objective #{gid} completed (+30 XP)');self.conn.commit();return True
  return False
 def delete_goal(self,gid):
  cur=self.conn.execute('DELETE FROM goals WHERE id=? AND completed=0',(gid,))
  if cur.rowcount:self._event('goal_removed',f'Active objective #{gid} removed');self.conn.commit();return True
  return False
 def add_habit(self,title):
  title=title.strip()[:80]
  if not title:raise ValueError('Habit name cannot be empty')
  self.conn.execute('INSERT INTO habits(title,created_at) VALUES(?,?)',(title,datetime.now().isoformat(timespec='seconds')));self._event('habit_created',f'Habit added: {title}');self.conn.commit()
 def habits(self):
  today=date.today().isoformat()
  return [dict(r) for r in self.conn.execute('''SELECT h.*,EXISTS(SELECT 1 FROM habit_logs l WHERE l.habit_id=h.id AND l.day=?) AS done_today,(SELECT COUNT(*) FROM habit_logs l WHERE l.habit_id=h.id) AS total_completions FROM habits h WHERE h.active=1 ORDER BY h.id DESC''',(today,))]
 def complete_habit(self,hid):
  try:self.conn.execute('INSERT INTO habit_logs(habit_id,day,completed_at) VALUES(?,?,?)',(hid,date.today().isoformat(),datetime.now().isoformat(timespec='seconds')))
  except sqlite3.IntegrityError:return False
  self.conn.execute('UPDATE player SET xp=xp+10,coins=coins+2 WHERE id=1');self._event('habit_completed',f'Habit #{hid} completed (+10 XP)');self.conn.commit();return True
 def archive_habit(self,hid):
  cur=self.conn.execute('UPDATE habits SET active=0 WHERE id=? AND active=1',(hid,))
  if cur.rowcount:self._event('habit_archived',f'Habit #{hid} archived');self.conn.commit();return True
  return False
 def save_reflection(self,note):
  note=note.strip()[:4000];today=date.today().isoformat()
  self.conn.execute('INSERT INTO reflections(day,note,updated_at) VALUES(?,?,?) ON CONFLICT(day) DO UPDATE SET note=excluded.note,updated_at=excluded.updated_at',(today,note,datetime.now().isoformat(timespec='seconds')));self._event('reflection_saved','Daily reflection updated');self.conn.commit()
 def reflection(self,day=None):
  row=self.conn.execute('SELECT note FROM reflections WHERE day=?',(day or date.today().isoformat(),)).fetchone();return row['note'] if row else ''
 def recent_events(self,limit=100):return [dict(r) for r in self.conn.execute('SELECT * FROM events ORDER BY id DESC LIMIT ?',(max(1,min(1000,int(limit))),))]
 def stats(self):
  week=(date.today()-timedelta(days=6)).isoformat()
  return {'completed_quests':self.conn.execute("SELECT COUNT(*) FROM events WHERE kind='quest_completed'").fetchone()[0],'completed_goals':self.conn.execute("SELECT COUNT(*) FROM events WHERE kind='goal_completed'").fetchone()[0],'completed_habits':self.conn.execute("SELECT COUNT(*) FROM events WHERE kind='habit_completed'").fetchone()[0],'active_goals':self.conn.execute('SELECT COUNT(*) FROM goals WHERE completed=0').fetchone()[0],'active_habits':self.conn.execute('SELECT COUNT(*) FROM habits WHERE active=1').fetchone()[0],'event_count':self.conn.execute('SELECT COUNT(*) FROM events').fetchone()[0],'player':self.player()}
 def backup(self,destination):
  dest=Path(destination);dest.parent.mkdir(parents=True,exist_ok=True);target=sqlite3.connect(dest)
  try:self.conn.backup(target)
  finally:target.close()
  return dest
 def export_json(self,destination):
  dest=Path(destination);dest.parent.mkdir(parents=True,exist_ok=True);tables={}
  for table in ('player','attributes','quests','events','goals','habits','habit_logs','reflections'):tables[table]=[dict(r) for r in self.conn.execute(f'SELECT * FROM {table}')]
  dest.write_text(json.dumps({'app':'ECLIPSE','format_version':2,'exported_at':datetime.now().isoformat(timespec='seconds'),'tables':tables},ensure_ascii=False,indent=2),encoding='utf-8');return dest
 def import_json(self,source):
  data=json.loads(Path(source).read_text(encoding='utf-8'))
  if data.get('app')!='ECLIPSE' or data.get('format_version')!=2 or not isinstance(data.get('tables'),dict):raise ValueError('This is not a supported ECLIPSE 2.0 export.')
  tables=data['tables'];required={'player','attributes','quests','events','goals','habits','habit_logs','reflections'}
  if not required.issubset(tables):raise ValueError('Backup is incomplete.')
  p=tables['player'][0];name=str(p['name'])[:40];xp=max(0,int(p['xp']));coins=max(0,int(p['coins']))
  if not isinstance(tables['attributes'],list) or any(a.get('name') not in ATTRIBUTES for a in tables['attributes']):raise ValueError('Backup contains invalid attributes.')
  with self.conn:
   for t in ('habit_logs','habits','reflections','goals','quests','events','attributes'):self.conn.execute(f'DELETE FROM {t}')
   self.conn.execute('UPDATE player SET name=?,xp=?,coins=? WHERE id=1',(name,xp,coins))
   for t in ('attributes','quests','events','goals','habits','habit_logs','reflections'):
    cols=[r[1] for r in self.conn.execute(f'PRAGMA table_info({t})')]
    for row in tables[t]:self.conn.execute(f"INSERT INTO {t} ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",[row.get(c) for c in cols])
   self._event('backup_restored','Progress restored from an ECLIPSE 2.0 export')
 def close(self):self.conn.close()
