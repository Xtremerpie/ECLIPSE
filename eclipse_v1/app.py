"""ECLIPSE 2.0 lightweight Tkinter desktop application."""
from __future__ import annotations
import os, sys
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from .engine import EclipseEngine, ATTRIBUTES
from .brain import SystemBrain

BG='#080d18'; PANEL='#111b2d'; PANEL2='#17263b'; CYAN='#55e6f2'; TEXT='#e7f2ff'; MUTED='#8da3b8'; GREEN='#9ce6b0'; RED='#ff8c8c'
class EclipseApp:
 def __init__(self,root):
  self.root=root;self.root.title('ECLIPSE 2.0 — The Complete System');self.root.geometry('1080x700');self.root.minsize(820,560);self.root.configure(bg=BG)
  self.data_dir=Path.home()/'.eclipse';self.data_dir.mkdir(exist_ok=True);self.engine=EclipseEngine(self.data_dir/'eclipse_v2.db',Path.cwd()/'eclipse_save.json',Path.cwd()/'eclipse_v1.db');self.brain=SystemBrain(self.engine)
  self.timer_job=None;self.timer_remaining=25*60;self.timer_running=False
  self._style();self._layout();self.refresh_all();self.root.protocol('WM_DELETE_WINDOW',self.close)
 def _style(self):
  s=ttk.Style();s.theme_use('clam');s.configure('TNotebook',background=BG,borderwidth=0);s.configure('TNotebook.Tab',background=PANEL2,foreground=TEXT,padding=(12,9),font=('Segoe UI',9,'bold'));s.map('TNotebook.Tab',background=[('selected','#214054')],foreground=[('selected',CYAN)])
  s.configure('Treeview',background=PANEL,fieldbackground=PANEL,foreground=TEXT,rowheight=30,borderwidth=0,font=('Segoe UI',9));s.configure('Treeview.Heading',background=PANEL2,foreground=CYAN,font=('Segoe UI',9,'bold'));s.map('Treeview',background=[('selected','#244456')]);s.configure('TProgressbar',troughcolor=PANEL2,background=CYAN)
 def _button(self,parent,text,cmd,color='#153b4b',fg=CYAN):return tk.Button(parent,text=text,command=cmd,bg=color,fg=fg,activebackground='#24566a',activeforeground='white',relief='flat',bd=0,padx=13,pady=8,font=('Segoe UI',9,'bold'),cursor='hand2')
 def _text(self,parent,height=10):return tk.Text(parent,bg=PANEL,fg=TEXT,insertbackground=TEXT,relief='flat',wrap='word',font=('Segoe UI',10),padx=12,pady=10,height=height)
 def _layout(self):
  header=tk.Frame(self.root,bg=BG,padx=22,pady=13);header.pack(fill='x');tk.Label(header,text='E C L I P S E',bg=BG,fg=CYAN,font=('Segoe UI',24,'bold')).pack(anchor='w');tk.Label(header,text='THE COMPLETE SYSTEM  /  LOCAL INSTANCE  /  V2.0',bg=BG,fg=MUTED,font=('Consolas',9)).pack(anchor='w')
  self.profile_bar=tk.Frame(self.root,bg=PANEL,padx=16,pady=10);self.profile_bar.pack(fill='x',padx=22,pady=(0,12));self.profile_label=tk.Label(self.profile_bar,bg=PANEL,fg=TEXT,font=('Segoe UI',10),justify='left');self.profile_label.pack(anchor='w')
  self.tabs=ttk.Notebook(self.root);self.tabs.pack(fill='both',expand=True,padx=22,pady=(0,12));self.pages={}
  for title,key in [('DASHBOARD','dashboard'),('QUESTS','quests'),('GOALS','goals'),('HABITS','habits'),('FOCUS','focus'),('GROWTH','growth'),('STORY','story'),('JOURNAL','journal'),('HISTORY','history'),('SETTINGS','settings')]:
   f=tk.Frame(self.tabs,bg=BG);self.pages[key]=f;self.tabs.add(f,text=title)
  self._build_dashboard();self._build_quests();self._build_goals();self._build_habits();self._build_focus();self._build_growth();self._build_story();self._build_journal();self._build_history();self._build_settings()
  tk.Label(self.root,text='YOUR CHOICES. YOUR PACE. YOUR PROGRESS.  ·  OFFLINE-FIRST',bg=BG,fg=MUTED,font=('Consolas',8)).pack(pady=(0,7))
 def _heading(self,key,title,sub=''):
  p=self.pages[key];tk.Label(p,text=title,bg=BG,fg=CYAN,font=('Segoe UI',15,'bold')).pack(anchor='w',padx=16,pady=(14,2))
  if sub:tk.Label(p,text=sub,bg=BG,fg=MUTED,font=('Segoe UI',9)).pack(anchor='w',padx=16,pady=(0,10))
 def _tree(self,parent,columns,headings,widths,height=10,show='headings'):
  wrap=tk.Frame(parent,bg=BG);wrap.pack(fill='both',expand=True,padx=16,pady=8);tree=ttk.Treeview(wrap,columns=columns,show=show,height=height)
  for c,h,w in zip(columns,headings,widths):tree.heading(c,text=h);tree.column(c,width=w,anchor='w' if c in ('title','objective','name') else 'center')
  y=ttk.Scrollbar(wrap,orient='vertical',command=tree.yview);tree.configure(yscrollcommand=y.set);tree.pack(side='left',fill='both',expand=True);y.pack(side='right',fill='y');return tree
 def _build_dashboard(self):
  self._heading('dashboard','SYSTEM OVERVIEW','A clear view of the progress you chose to record.')
  cards=tk.Frame(self.pages['dashboard'],bg=BG);cards.pack(fill='x',padx=16,pady=8);self.metric_labels={}
  for key,label in [('level','LEVEL'),('rank','RANK'),('xp','TOTAL XP'),('coins','COINS'),('quests','QUESTS DONE'),('goals','GOALS DONE')]:
   card=tk.Frame(cards,bg=PANEL,padx=14,pady=12);card.pack(side='left',fill='x',expand=True,padx=4);tk.Label(card,text=label,bg=PANEL,fg=MUTED,font=('Consolas',8,'bold')).pack(anchor='w');v=tk.Label(card,text='—',bg=PANEL,fg=CYAN,font=('Segoe UI',17,'bold'));v.pack(anchor='w');self.metric_labels[key]=v
  self.level_label=tk.Label(self.pages['dashboard'],text='',bg=BG,fg=TEXT,font=('Segoe UI',10));self.level_label.pack(anchor='w',padx=22,pady=(12,4));self.level_bar=ttk.Progressbar(self.pages['dashboard'],maximum=100);self.level_bar.pack(fill='x',padx=22,pady=(0,12))
  self.attr_frame=tk.Frame(self.pages['dashboard'],bg=BG);self.attr_frame.pack(fill='x',padx=16,pady=4);self.dashboard_report=self._text(self.pages['dashboard'],8);self.dashboard_report.pack(fill='both',expand=True,padx=16,pady=10);self.dashboard_report.configure(state='disabled')
 def _build_quests(self):
  self._heading('quests','DAILY DIRECTIVES','Complete a task only when you have genuinely done it. Custom quests are available too.')
  self.quest_tree=self._tree(self.pages['quests'],('title','category','xp','state'),('DIRECTIVE','ATTRIBUTE','REWARD','STATUS'),(500,150,100,130),11)
  bar=tk.Frame(self.pages['quests'],bg=BG);bar.pack(fill='x',padx=16,pady=10);self._button(bar,'COMPLETE SELECTED',self.complete_quest,'#17432f',GREEN).pack(side='left',padx=(0,6));self._button(bar,'ADD CUSTOM QUEST',self.add_quest).pack(side='left',padx=6);self._button(bar,'REMOVE SELECTED',self.remove_quest,'#44252c',RED).pack(side='right')
 def _build_goals(self):
  self._heading('goals','LONG-TERM OBJECTIVES','Break meaningful projects into milestones. Completing one awards a one-time reward.')
  self.goal_tree=self._tree(self.pages['goals'],('state','created'),('STATUS','CREATED'),(150,180),11,show='tree headings');self.goal_tree.heading('#0',text='OBJECTIVE');self.goal_tree.column('#0',width=600,anchor='w')
  bar=tk.Frame(self.pages['goals'],bg=BG);bar.pack(fill='x',padx=16,pady=10);self._button(bar,'ADD OBJECTIVE',self.add_goal).pack(side='left');self._button(bar,'MARK COMPLETE',self.complete_goal,'#17432f',GREEN).pack(side='left',padx=8);self._button(bar,'REMOVE ACTIVE',self.remove_goal,'#44252c',RED).pack(side='right')
 def _build_habits(self):
  self._heading('habits','HABIT TRACKER','Check in once per day. Missed days never remove progress or trigger penalties.')
  self.habit_tree=self._tree(self.pages['habits'],('title','today','total'),('HABIT','TODAY','TOTAL CHECK-INS'),(550,180,180),11)
  bar=tk.Frame(self.pages['habits'],bg=BG);bar.pack(fill='x',padx=16,pady=10);self._button(bar,'ADD HABIT',self.add_habit).pack(side='left');self._button(bar,'CHECK IN TODAY',self.complete_habit,'#17432f',GREEN).pack(side='left',padx=8);self._button(bar,'ARCHIVE HABIT',self.archive_habit,'#44252c',RED).pack(side='right')
 def _build_focus(self):
  self._heading('focus','FOCUS ROOM','A simple local focus timer. It does not track your activity or award automatic XP.')
  card=tk.Frame(self.pages['focus'],bg=PANEL,padx=26,pady=24);card.pack(padx=40,pady=28,fill='x');self.timer_display=tk.Label(card,text='25:00',bg=PANEL,fg=CYAN,font=('Segoe UI',44,'bold'));self.timer_display.pack(pady=10)
  row=tk.Frame(card,bg=PANEL);row.pack(pady=8);self._button(row,'START',self.start_timer,'#17432f',GREEN).pack(side='left',padx=5);self._button(row,'PAUSE',self.pause_timer).pack(side='left',padx=5);self._button(row,'RESET',self.reset_timer,'#44252c',RED).pack(side='left',padx=5)
  row2=tk.Frame(card,bg=PANEL);row2.pack(pady=12);tk.Label(row2,text='SESSION LENGTH',bg=PANEL,fg=MUTED).pack(side='left',padx=8);self.timer_choice=tk.StringVar(value='25 minutes');combo=ttk.Combobox(row2,textvariable=self.timer_choice,values=['5 minutes','15 minutes','25 minutes','45 minutes','60 minutes'],state='readonly',width=14);combo.pack(side='left');combo.bind('<<ComboboxSelected>>',lambda e:self.reset_timer())
  self.timer_hint=tk.Label(self.pages['focus'],text='Choose a comfortable session. Breaks are allowed.',bg=BG,fg=MUTED,font=('Segoe UI',10));self.timer_hint.pack(pady=10)
 def _build_growth(self):
  self._heading('growth','SYSTEM BRAIN & CHARACTER GROWTH','Insights are based only on your explicit ECLIPSE records.')
  self.growth_text=self._text(self.pages['growth'],22);self.growth_text.pack(fill='both',expand=True,padx=16,pady=8);self.growth_text.configure(state='disabled')
 def _build_story(self):
  self._heading('story','THE UNKNOWN EXISTENCE','Original story fragments unlock through recorded progress.')
  self.story_text=self._text(self.pages['story'],22);self.story_text.pack(fill='both',expand=True,padx=16,pady=8);self.story_text.configure(state='disabled')
 def _build_journal(self):
  self._heading('journal','DAILY REFLECTION','Private note stored locally on this PC. Keep it simple; there is no score.')
  self.journal_text=self._text(self.pages['journal'],16);self.journal_text.pack(fill='both',expand=True,padx=16,pady=8);self._button(self.pages['journal'],"SAVE TODAY'S REFLECTION",self.save_reflection,'#17432f',GREEN).pack(anchor='e',padx=16,pady=10)
 def _build_history(self):
  self._heading('history','SYSTEM MEMORY','Recent actions recorded inside ECLIPSE. No desktop monitoring.')
  self.history_text=self._text(self.pages['history'],22);self.history_text.pack(fill='both',expand=True,padx=16,pady=8);self.history_text.configure(state='disabled')
 def _build_settings(self):
  self._heading('settings','SYSTEM SETTINGS & DATA','Your database stays on this PC. Back up before moving or restoring progress.')
  p=self.pages['settings'];self.settings_status=tk.Label(p,text=f'Data folder: {self.data_dir}\nDatabase: {self.engine.db_path}',bg=BG,fg=MUTED,justify='left',font=('Consolas',9));self.settings_status.pack(anchor='w',padx=18,pady=10)
  grid=tk.Frame(p,bg=BG);grid.pack(anchor='w',padx=16,pady=6)
  items=[('CHANGE PLAYER NAME',self.rename_player,'#153b4b',CYAN),('BACK UP DATABASE',self.backup_db,'#153b4b',CYAN),('EXPORT PORTABLE JSON',self.export_json,'#153b4b',CYAN),('RESTORE FROM JSON',self.import_json,'#44252c',RED),('RUN SYSTEM CHECK',self.system_check,'#17432f',GREEN),('OPEN DATA FOLDER',self.open_data_folder,'#153b4b',CYAN)]
  for i,(label,cmd,col,fg) in enumerate(items):self._button(grid,label,cmd,col,fg).grid(row=i//2,column=i%2,padx=6,pady=6,sticky='ew')
  grid.columnconfigure(0,minsize=220);grid.columnconfigure(1,minsize=220);self.check_text=self._text(p,8);self.check_text.pack(fill='both',expand=True,padx=16,pady=12);self.check_text.insert('1.0','Run System Check to validate the local database, quest board, progression calculations, and backup capability.');self.check_text.configure(state='disabled')
 def _set_text(self,w,value):w.configure(state='normal');w.delete('1.0','end');w.insert('1.0',value);w.configure(state='disabled')
 def refresh_all(self):
  report=self.brain.snapshot();p=report['player'];stats=self.engine.stats();self.profile_label.configure(text=f"PLAYER  {p['name']}     RANK  {p['rank']}     LEVEL  {p['level']}     XP  {p['level_xp']} / {p['next_xp']}     COINS  {p['coins']}")
  for k,v in [('level',p['level']),('rank',p['rank']),('xp',p['xp']),('coins',p['coins']),('quests',stats['completed_quests']),('goals',stats['completed_goals'])]:self.metric_labels[k].configure(text=str(v))
  pct=p['level_xp']/p['next_xp']*100 if p['next_xp'] else 0;self.level_label.configure(text=f"LEVEL {p['level']} PROGRESS  ·  {p['level_xp']} / {p['next_xp']} XP");self.level_bar['value']=pct
  for child in self.attr_frame.winfo_children():child.destroy()
  for name,val in p['attributes'].items():
   c=tk.Frame(self.attr_frame,bg=PANEL,padx=9,pady=6);c.pack(side='left',fill='x',expand=True,padx=3);tk.Label(c,text=name.upper(),bg=PANEL,fg=MUTED,font=('Consolas',7,'bold')).pack(anchor='w');tk.Label(c,text=str(val),bg=PANEL,fg=CYAN,font=('Segoe UI',13,'bold')).pack(anchor='w')
  dash=f"SYSTEM STATUS: ONLINE · LOCAL MODE\n\n{report['recommendation']}\n\nACTIVE OBJECTIVES: {stats['active_goals']}   ACTIVE HABITS: {stats['active_habits']}\nRECORDED QUESTS: {stats['completed_quests']}   HABIT CHECK-INS: {stats['completed_habits']}\n\nREMINDER: This is a progress tool, not a measure of your worth. Rest and changing goals are allowed.";self._set_text(self.dashboard_report,dash)
  for t in (self.quest_tree,self.goal_tree,self.habit_tree):
   for item in t.get_children():t.delete(item)
  for q in self.engine.quests():self.quest_tree.insert('','end',iid=str(q['id']),values=(q['title'],q['category'],f"+{q['xp']} XP",'COMPLETED' if q['completed'] else 'AVAILABLE'))
  for g in self.engine.goals():self.goal_tree.insert('','end',iid=str(g['id']),text=g['title'],values=('COMPLETED' if g['completed'] else 'ACTIVE',g['created_at'][:10]))
  for h in self.engine.habits():self.habit_tree.insert('','end',iid=str(h['id']),values=(h['title'],'DONE' if h['done_today'] else 'NOT YET',h['total_completions']))
  ach='\n'.join(f"{'[UNLOCKED]' if a['unlocked'] else '[LOCKED]'}  {a['title']} — {a['description']}" for a in report['achievements']);skills='\n'.join(f"{'[UNLOCKED]' if s['unlocked'] else '[LOCKED]'}  {s['title']} · {s['attribute']} {s['value']}/3" for s in report['skills']);attrs='\n'.join(f"{k}: {v}" for k,v in p['attributes'].items())
  growth=f"SYSTEM ANALYSIS\n{report['recommendation']}\n\nSTRONGEST RECORDED ATTRIBUTE: {report['strongest_attribute']}\nLEAST PRACTISED ATTRIBUTE: {report['weakest_attribute']}\n\nATTRIBUTES\n{attrs}\n\nACHIEVEMENTS\n{ach}\n\nSKILL EVOLUTION\n{skills}\n\nSTATISTICS\nCompleted directives: {stats['completed_quests']}\nCompleted objectives: {stats['completed_goals']}\nHabit check-ins: {stats['completed_habits']}\nTotal archived events: {stats['event_count']}\n\nThe System Brain is read-only. It does not monitor your device or award XP.";self._set_text(self.growth_text,growth)
  story='\n\n'.join(f"{c['title']}  [{'UNLOCKED' if c['unlocked'] else 'LOCKED · '+str(c['required_records'])+' directives required'}]\n{c['body'] if c['unlocked'] else 'This archive fragment has not yet been released.'}" for c in report['chapters']);self._set_text(self.story_text,story)
  hist='\n\n'.join(f"[{e['created_at']}]  {e['kind'].upper()}\n{e['detail']}" for e in self.engine.recent_events(150));self._set_text(self.history_text,hist or 'No events recorded yet.')
  self.journal_text.delete('1.0','end');self.journal_text.insert('1.0',self.engine.reflection())
 def _selected(self,tree):
  sel=tree.selection()
  if not sel:messagebox.showinfo('ECLIPSE','Select an item first.',parent=self.root);return None
  return int(sel[0])
 def complete_quest(self):
  i=self._selected(self.quest_tree)
  if i is not None:
   if self.engine.complete_quest(i):self.refresh_all();messagebox.showinfo('SYSTEM','Record accepted. Progress updated.',parent=self.root)
   else:messagebox.showinfo('SYSTEM','This directive is already completed or unavailable.',parent=self.root)
 def add_quest(self):
  title=simpledialog.askstring('Custom directive','What task do you want to add?',parent=self.root)
  if not title:return
  category=simpledialog.askstring('Attribute','Choose one: '+', '.join(ATTRIBUTES),initialvalue='Focus',parent=self.root)
  if not category:return
  category=next((a for a in ATTRIBUTES if a.lower()==category.strip().lower()),None)
  if not category:messagebox.showerror('ECLIPSE','Unknown attribute.',parent=self.root);return
  xp=simpledialog.askinteger('Reward','Choose XP reward (5–50).',initialvalue=20,minvalue=5,maxvalue=50,parent=self.root)
  if xp is None:return
  try:self.engine.add_custom_quest(title,category,xp);self.refresh_all()
  except Exception as e:messagebox.showerror('ECLIPSE',str(e),parent=self.root)
 def remove_quest(self):
  i=self._selected(self.quest_tree)
  if i is not None and messagebox.askyesno('Remove directive','Remove this uncompleted directive?',parent=self.root):
   if self.engine.delete_quest(i):self.refresh_all()
 def add_goal(self):
  title=simpledialog.askstring('New objective','What meaningful objective do you want to work toward?',parent=self.root)
  if title:
   try:self.engine.add_goal(title);self.refresh_all()
   except Exception as e:messagebox.showerror('ECLIPSE',str(e),parent=self.root)
 def complete_goal(self):
  i=self._selected(self.goal_tree)
  if i is not None and messagebox.askyesno('Confirm milestone','Have you genuinely completed this objective?',parent=self.root):
   if self.engine.complete_goal(i):self.refresh_all();messagebox.showinfo('SYSTEM','Milestone recorded. +30 XP',parent=self.root)
   else:messagebox.showinfo('SYSTEM','This objective is already complete.',parent=self.root)
 def remove_goal(self):
  i=self._selected(self.goal_tree)
  if i is not None and messagebox.askyesno('Remove objective','Remove this active objective?',parent=self.root):self.engine.delete_goal(i);self.refresh_all()
 def add_habit(self):
  title=simpledialog.askstring('New habit','Name a small habit you want to track.',parent=self.root)
  if title:
   try:self.engine.add_habit(title);self.refresh_all()
   except Exception as e:messagebox.showerror('ECLIPSE',str(e),parent=self.root)
 def complete_habit(self):
  i=self._selected(self.habit_tree)
  if i is not None:
   if self.engine.complete_habit(i):self.refresh_all();messagebox.showinfo('SYSTEM','Daily check-in recorded. +10 XP',parent=self.root)
   else:messagebox.showinfo('SYSTEM','This habit already has a check-in for today.',parent=self.root)
 def archive_habit(self):
  i=self._selected(self.habit_tree)
  if i is not None and messagebox.askyesno('Archive habit','Hide this habit from the active tracker? Past check-ins stay saved.',parent=self.root):self.engine.archive_habit(i);self.refresh_all()
 def _timer_tick(self):
  if not self.timer_running:return
  self.timer_remaining-=1;self._show_timer()
  if self.timer_remaining<=0:
   self.timer_running=False;self.timer_job=None;self.timer_hint.configure(text='Session complete. Take a break if you need one.');self.root.bell();messagebox.showinfo('Focus Room','Your focus session is complete.',parent=self.root);return
  self.timer_job=self.root.after(1000,self._timer_tick)
 def _show_timer(self):self.timer_display.configure(text=f'{self.timer_remaining//60:02d}:{self.timer_remaining%60:02d}')
 def start_timer(self):
  if self.timer_running:return
  self.timer_running=True;self.timer_hint.configure(text='Timer running locally. You can pause or reset at any time.');self._timer_tick()
 def pause_timer(self):
  self.timer_running=False
  if self.timer_job:self.root.after_cancel(self.timer_job);self.timer_job=None
  self.timer_hint.configure(text='Paused. Continue when you are ready.')
 def reset_timer(self):
  self.pause_timer();self.timer_remaining=int(self.timer_choice.get().split()[0])*60;self._show_timer();self.timer_hint.configure(text='Timer reset. Choose a comfortable pace.')
 def save_reflection(self):self.engine.save_reflection(self.journal_text.get('1.0','end').strip());self.refresh_all();messagebox.showinfo('Journal','Reflection saved locally.',parent=self.root)
 def rename_player(self):
  name=simpledialog.askstring('Player profile','Choose your player name:',initialvalue=self.engine.player()['name'],parent=self.root)
  if name:
   try:self.engine.rename_player(name);self.refresh_all()
   except Exception as e:messagebox.showerror('ECLIPSE',str(e),parent=self.root)
 def backup_db(self):
  path=filedialog.asksaveasfilename(parent=self.root,title='Save ECLIPSE database backup',defaultextension='.db',initialfile=f"eclipse_backup_{datetime.now():%Y%m%d_%H%M}.db",filetypes=[('SQLite database','*.db')])
  if path:
   try:self.engine.backup(path);messagebox.showinfo('Backup',f'Backup saved:\n{path}',parent=self.root)
   except Exception as e:messagebox.showerror('Backup failed',str(e),parent=self.root)
 def export_json(self):
  path=filedialog.asksaveasfilename(parent=self.root,title='Export ECLIPSE progress',defaultextension='.json',initialfile='eclipse_export.json',filetypes=[('JSON backup','*.json')])
  if path:
   try:self.engine.export_json(path);messagebox.showinfo('Export complete',f'Portable backup saved:\n{path}',parent=self.root)
   except Exception as e:messagebox.showerror('Export failed',str(e),parent=self.root)
 def import_json(self):
  path=filedialog.askopenfilename(parent=self.root,title='Choose ECLIPSE 2.0 JSON backup',filetypes=[('JSON backup','*.json')])
  if not path:return
  if not messagebox.askyesno('Restore progress','This replaces the current ECLIPSE records. A safety backup will be created first. Continue?',parent=self.root):return
  try:
   safety=self.data_dir/f"pre_restore_{datetime.now():%Y%m%d_%H%M%S}.db";self.engine.backup(safety);self.engine.import_json(path);self.refresh_all();messagebox.showinfo('Restore complete',f'Progress restored. Safety backup:\n{safety}',parent=self.root)
  except Exception as e:messagebox.showerror('Restore failed',f'{e}\nYour safety backup is retained if it was created.',parent=self.root)
 def system_check(self):
  checks=[]
  try:checks.append(('Database connection',self.engine.conn.execute('SELECT 1').fetchone()[0]==1))
  except Exception:checks.append(('Database connection',False))
  try:checks.append(('Player profile',bool(self.engine.player()['name'])))
  except Exception:checks.append(('Player profile',False))
  try:checks.append(('Daily quest board',len(self.engine.quests())>=5))
  except Exception:checks.append(('Daily quest board',False))
  try:
   p=self.engine.player();checks.append(('XP progression',p['next_xp']>0 and p['level']>=1))
  except Exception:checks.append(('XP progression',False))
  try:
   temp=self.data_dir/'diagnostic_backup.db';self.engine.backup(temp);ok=temp.exists() and temp.stat().st_size>0;checks.append(('Database backup',ok));temp.unlink(missing_ok=True)
  except Exception:checks.append(('Database backup',False))
  try:checks.append(('SQLite integrity',self.engine.conn.execute('PRAGMA integrity_check').fetchone()[0]=='ok'))
  except Exception:checks.append(('SQLite integrity',False))
  out='ECLIPSE SYSTEM CHECK\n'+'='*32+'\n'+'\n'.join(('PASS  ' if ok else 'FAIL  ')+name for name,ok in checks)+f"\n\nRESULT: {sum(ok for _,ok in checks)}/{len(checks)} checks passed.\nPython: {sys.version.split()[0]}\nPlatform: {sys.platform}\nTk: {self.root.tk.call('info','patchlevel')}\nData: {self.engine.db_path}";self._set_text(self.check_text,out)
 def open_data_folder(self):
  try:
   if sys.platform=='win32':os.startfile(self.data_dir)
   elif sys.platform=='darwin':os.system(f'open "{self.data_dir}"')
   else:os.system(f'xdg-open "{self.data_dir}"')
  except Exception as e:messagebox.showerror('ECLIPSE',str(e),parent=self.root)
 def close(self):
  if self.timer_job:
   try:self.root.after_cancel(self.timer_job)
   except Exception:pass
  self.engine.close();self.root.destroy()
def main():
 root=tk.Tk();EclipseApp(root);root.mainloop()
if __name__=='__main__':main()
