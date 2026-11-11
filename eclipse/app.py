"""ECLIPSE 3.1 — a polished, local-first personal progression system."""
from __future__ import annotations
import os, sys, base64, math
from datetime import date, datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from .engine import EclipseEngine, ATTRIBUTES
from .brain import SystemBrain
BG="#090D18"; SIDE="#0D1423"; PANEL="#121D30"; PANEL2="#192840"; LINE="#263751"
ACCENT="#77E5E8"; VIOLET="#9B8CFF"; GOLD="#F2C879"; TEXT="#EEF4FF"; MUTED="#91A2BB"; GREEN="#8FE0B2"; RED="#F28C9A"; FONT="Segoe UI"

class EclipseApp:
    NAV=[("OVERVIEW","dashboard","◈"),("DAILY DIRECTIVES","quests","✦"),("OBJECTIVES","goals","◎"),("HABITS","habits","↗"),("FOCUS ROOM","focus","◷"),("SYSTEM INTELLIGENCE","growth","⌁"),("STORY ARCHIVE","story","▤"),("DAILY JOURNAL","journal","✎"),("ACTIVITY LOG","history","≡"),("SYSTEM SETTINGS","settings","⚙")]
    def __init__(self,root):
        self.root=root;root.title("ECLIPSE 3.1 | Personal Progression System");root.geometry("1320x850");root.minsize(980,680);root.configure(bg=BG)
        self.data_dir=Path.home()/".eclipse";self.data_dir.mkdir(exist_ok=True)
        self.engine=EclipseEngine(self.data_dir/"eclipse_v2.db",Path.cwd()/"eclipse_save.json",Path.cwd()/"eclipse_v1.db")
        self.brain=SystemBrain(self.engine);self.pages={};self.page_containers={};self.page_canvases={};self.nav_buttons={};self.timer_job=None;self.timer_remaining=1500;self.timer_elapsed=0;self.timer_running=False
        self.app_icon=self._make_icon();root.iconphoto(True,self.app_icon);self._style();self._shell();self._build_pages();self.engine.log_session("app_opened","ECLIPSE opened on this device")
        self.refresh_all();self.show_page("dashboard");root.protocol("WM_DELETE_WINDOW",self.close)
        if self.engine.get_setting("auto_checkin","1")=="1":root.after(700,self._maybe_daily_checkin)
    def _make_icon(self):
        size=32;pixels=bytearray()
        for y in range(size):
            for x in range(size):
                dx=x-16;dy=y-16;r=math.sqrt(dx*dx+dy*dy)
                rgb=(9,13,24)
                if 10.5<=r<=13.2:rgb=(155,140,255)
                if r<=10.5:rgb=(28,47,72)
                if ((x-18.5)**2+(y-14.5)**2<=8.5**2 and not ((x-22.5)**2+(y-10.5)**2<=8.5**2)):rgb=(119,229,232)
                pixels.extend(rgb)
        ppm=f"P6\\n{size} {size}\\n255\\n".encode()+bytes(pixels)
        return tk.PhotoImage(data=base64.b64encode(ppm).decode("ascii"))
    def _style(self):
        s=ttk.Style();s.theme_use("clam")
        s.configure("Treeview",background=PANEL,fieldbackground=PANEL,foreground=TEXT,rowheight=34,borderwidth=0,font=(FONT,9))
        s.configure("Treeview.Heading",background=PANEL2,foreground=ACCENT,relief="flat",font=(FONT,8,"bold"),padding=(8,9))
        s.map("Treeview",background=[("selected","#28435B")],foreground=[("selected",TEXT)])
        s.configure("TScrollbar",background=PANEL2,troughcolor=BG,bordercolor=BG,arrowcolor=MUTED)
        s.configure("Eclipse.Horizontal.TProgressbar",troughcolor=PANEL2,background=ACCENT,bordercolor=PANEL2,lightcolor=ACCENT,darkcolor=ACCENT)
        s.configure("TCombobox",fieldbackground=PANEL2,background=PANEL2,foreground=TEXT,arrowcolor=ACCENT,padding=7)
        s.map("TCombobox",fieldbackground=[("readonly",PANEL2)],foreground=[("readonly",TEXT)])
    def _shell(self):
        shell=tk.Frame(self.root,bg=BG);shell.pack(fill="both",expand=True)
        side=tk.Frame(shell,bg=SIDE,width=238);side.pack(side="left",fill="y");side.pack_propagate(False)
        brand=tk.Frame(side,bg=SIDE,padx=20,pady=22);brand.pack(fill="x")
        mark=tk.Canvas(brand,width=42,height=42,bg=SIDE,highlightthickness=0);mark.pack(side="left",padx=(0,11))
        mark.create_oval(3,3,39,39,outline=VIOLET,width=2);mark.create_oval(10,8,34,34,fill=ACCENT,outline=ACCENT);mark.create_oval(18,4,39,27,fill=SIDE,outline=SIDE)
        tk.Label(brand,text="ECLIPSE",bg=SIDE,fg=TEXT,font=(FONT,17,"bold")).pack(anchor="w",pady=(2,0))
        tk.Label(brand,text="PERSONAL SYSTEM  /  03",bg=SIDE,fg=MUTED,font=(FONT,7,"bold")).pack(anchor="w")
        chip=tk.Frame(side,bg=PANEL,padx=13,pady=12);chip.pack(fill="x",padx=14,pady=(2,18))
        self.player_name=tk.Label(chip,text="PLAYER",bg=PANEL,fg=TEXT,font=(FONT,10,"bold"));self.player_name.pack(anchor="w")
        self.player_rank=tk.Label(chip,text="RANK F  ·  LEVEL 1",bg=PANEL,fg=ACCENT,font=(FONT,8,"bold"));self.player_rank.pack(anchor="w",pady=(4,0))
        tk.Label(side,text="COMMAND CENTER",bg=SIDE,fg=MUTED,font=(FONT,7,"bold")).pack(anchor="w",padx=21,pady=(0,7))
        nav=tk.Frame(side,bg=SIDE);nav.pack(fill="both",expand=True,padx=10)
        for label,key,symbol in self.NAV:
            b=tk.Button(nav,text=f"  {symbol}   {label}",anchor="w",command=lambda k=key:self.show_page(k),bg=SIDE,fg=MUTED,
                activebackground=PANEL2,activeforeground=TEXT,relief="flat",bd=0,padx=12,pady=10,font=(FONT,8,"bold"),cursor="hand2")
            b.pack(fill="x",pady=1);self.nav_buttons[key]=b
        foot=tk.Frame(side,bg=SIDE,padx=18,pady=15);foot.pack(fill="x")
        tk.Label(foot,text="LOCAL-FIRST  •  PRIVATE  •  YOUR PACE",bg=SIDE,fg=MUTED,font=(FONT,7)).pack(anchor="w")
        tk.Label(foot,text="●  SYSTEM ONLINE",bg=SIDE,fg=GREEN,font=(FONT,8,"bold")).pack(anchor="w",pady=(6,0))
        main=tk.Frame(shell,bg=BG);main.pack(side="left",fill="both",expand=True)
        top=tk.Frame(main,bg=BG,padx=28,pady=17);top.pack(fill="x")
        self.page_title=tk.Label(top,text="SYSTEM OVERVIEW",bg=BG,fg=TEXT,font=(FONT,18,"bold"));self.page_title.pack(side="left")
        right=tk.Frame(top,bg=BG);right.pack(side="right")
        self.date_label=tk.Label(right,text="",bg=BG,fg=MUTED,font=(FONT,9));self.date_label.pack(side="right",padx=(12,0))
        tk.Label(right,text="●  LOCAL INSTANCE",bg=BG,fg=GREEN,font=(FONT,8,"bold")).pack(side="right")
        self.content=tk.Frame(main,bg=BG);self.content.pack(fill="both",expand=True,padx=26,pady=(0,20))
        self.status=tk.Label(main,text="ECLIPSE 3.1  ·  DATA STORED ON THIS DEVICE",bg=BG,fg="#64748B",font=(FONT,7));self.status.pack(anchor="e",padx=28,pady=(0,9))
    def _page(self,key):
        outer=tk.Frame(self.content,bg=BG)
        canvas=tk.Canvas(outer,bg=BG,highlightthickness=0,bd=0)
        scroll=ttk.Scrollbar(outer,orient="vertical",command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right",fill="y");canvas.pack(side="left",fill="both",expand=True)
        inner=tk.Frame(canvas,bg=BG)
        window=canvas.create_window((0,0),window=inner,anchor="nw")
        inner.bind("<Configure>",lambda _e,c=canvas:c.configure(scrollregion=c.bbox("all")))
        canvas.bind("<Configure>",lambda e,c=canvas,w=window:c.itemconfigure(w,width=e.width))
        self.pages[key]=inner;self.page_containers[key]=outer;self.page_canvases[key]=canvas
        return inner
    def _on_mousewheel(self,event):
        widget_class=event.widget.winfo_class()
        if widget_class in ("Text","Treeview","Entry","TEntry","TCombobox","Spinbox"):return
        canvas=getattr(self,"_active_scroll_canvas",None)
        if canvas:canvas.yview_scroll(int(-1*(event.delta/120)),"units")
    def _on_mousewheel_linux(self,event):
        widget_class=event.widget.winfo_class()
        if widget_class in ("Text","Treeview","Entry","TEntry","TCombobox","Spinbox"):return
        canvas=getattr(self,"_active_scroll_canvas",None)
        if canvas:canvas.yview_scroll(-1 if event.num==4 else 1,"units")
    def _label(self,p,text,size=10,color=TEXT,bold=False,bg=PANEL,**kw):
        return tk.Label(p,text=text,bg=bg,fg=color,font=(FONT,size,"bold" if bold else "normal"),**kw)
    def _card(self,p,title=None,subtitle=None,bg=PANEL):
        f=tk.Frame(p,bg=bg,padx=17,pady=15,highlightthickness=1,highlightbackground=LINE)
        if title:self._label(f,title,9,ACCENT,True,bg).pack(anchor="w")
        if subtitle:self._label(f,subtitle,8,MUTED,bg).pack(anchor="w",pady=(4,10))
        return f
    def _button(self,p,text,cmd,kind="primary"):
        colors={"primary":(PANEL2,ACCENT),"success":("#183B35",GREEN),"danger":("#402632",RED),"quiet":(PANEL2,TEXT),"gold":("#403622",GOLD)}
        bg,fg=colors.get(kind,colors["primary"])
        return tk.Button(p,text=text,command=cmd,bg=bg,fg=fg,activebackground="#304762",activeforeground=TEXT,relief="flat",bd=0,padx=14,pady=9,font=(FONT,8,"bold"),cursor="hand2")
    def _heading(self,p,title,sub):
        self._label(p,title,17,TEXT,True,BG).pack(anchor="w",pady=(3,2));self._label(p,sub,9,MUTED,bg=BG).pack(anchor="w",pady=(0,16))
    def _tree(self,p,cols,heads,widths,height=11,show="headings"):
        wrap=tk.Frame(p,bg=BG);wrap.pack(fill="both",expand=True,pady=10);tree=ttk.Treeview(wrap,columns=cols,show=show,height=height)
        for c,h,w in zip(cols,heads,widths):tree.heading(c,text=h);tree.column(c,width=w,anchor="w" if c in ("title","objective","name") else "center")
        sc=ttk.Scrollbar(wrap,orient="vertical",command=tree.yview);tree.configure(yscrollcommand=sc.set);tree.pack(side="left",fill="both",expand=True);sc.pack(side="right",fill="y");return tree
    def _text(self,p,height=12):
        return tk.Text(p,height=height,bg=PANEL,fg=TEXT,insertbackground=TEXT,selectbackground="#34516D",relief="flat",wrap="word",padx=14,pady=12,font=(FONT,9),spacing1=3,spacing3=5)
    def _set_text(self,w,value):
        w.configure(state="normal");w.delete("1.0","end");w.insert("1.0",value);w.configure(state="disabled")
    def _build_pages(self):
        self._build_dashboard();self._build_quests();self._build_goals();self._build_habits();self._build_focus()
        self._build_growth();self._build_story();self._build_journal();self._build_history();self._build_settings()
    def _build_dashboard(self):
        p=self._page("dashboard");hero=tk.Frame(p,bg="#17243A",padx=22,pady=20,highlightthickness=1,highlightbackground="#34445E");hero.pack(fill="x",pady=(2,15))
        self.hero_greeting=tk.Label(hero,text="WELCOME BACK",bg="#17243A",fg=ACCENT,font=(FONT,8,"bold"));self.hero_greeting.pack(anchor="w")
        tk.Label(hero,text="Your next chapter starts here.",bg="#17243A",fg=TEXT,font=(FONT,20,"bold")).pack(anchor="w",pady=(5,3))
        tk.Label(hero,text="Small, honest actions create a clearer picture over time.",bg="#17243A",fg=MUTED,font=(FONT,9)).pack(anchor="w")
        bottom=tk.Frame(hero,bg="#17243A");bottom.pack(fill="x",pady=(16,0))
        self.level_line=tk.Label(bottom,text="LEVEL 1  ·  RANK F",bg="#17243A",fg=GOLD,font=(FONT,9,"bold"));self.level_line.pack(side="left")
        self.xp_line=tk.Label(bottom,text="0 / 100 XP",bg="#17243A",fg=MUTED,font=(FONT,8));self.xp_line.pack(side="right")
        self.level_bar=ttk.Progressbar(hero,maximum=100,style="Eclipse.Horizontal.TProgressbar");self.level_bar.pack(fill="x",pady=(9,0))
        metrics=tk.Frame(p,bg=BG);metrics.pack(fill="x",pady=(0,14));self.metric_labels={}
        for key,title,color in [("xp","TOTAL EXPERIENCE",ACCENT),("quests","DIRECTIVES DONE",VIOLET),("habits","HABIT CHECK-INS",GREEN),("focus","FOCUS MINUTES",GOLD)]:
            c=self._card(metrics,title);c.pack(side="left",fill="both",expand=True,padx=(0,9))
            v=self._label(c,"0",22,color,True,PANEL);v.pack(anchor="w",pady=(8,0));self.metric_labels[key]=v
        lower=tk.Frame(p,bg=BG);lower.pack(fill="both",expand=True)
        left=self._card(lower,"TODAY'S INTELLIGENCE","A grounded read of the records you chose to share.");left.pack(side="left",fill="both",expand=True,padx=(0,9))
        self.daily_insight=self._text(left,9);self.daily_insight.pack(fill="both",expand=True,pady=(12,0));self.daily_insight.configure(state="disabled")
        right=self._card(lower,"DAILY CHECK-IN","A short pulse helps the System understand your day.");right.pack(side="left",fill="both",expand=True,padx=(9,0))
        self.checkin_state=self._label(right,"NO CHECK-IN RECORDED TODAY",10,GOLD,True,PANEL);self.checkin_state.pack(anchor="w",pady=(15,8))
        self.checkin_detail=self._label(right,"Mood, energy and focus are optional signals—not grades.",8,MUTED,PANEL,justify="left",wraplength=360);self.checkin_detail.pack(anchor="w",pady=(0,14))
        row=tk.Frame(right,bg=PANEL);row.pack(anchor="w");self._button(row,"OPEN DAILY CHECK-IN",self.open_daily_checkin,"success").pack(side="left")
        self._button(row,"FULL ANALYSIS",lambda:self.show_page("growth"),"quiet").pack(side="left",padx=7)
        attrs=self._card(p,"ATTRIBUTE MATRIX","Skills grow from recorded practice—not from comparison with anyone else.")
        attrs.pack(fill="x",pady=(14,0));self.attribute_bars={}
        grid=tk.Frame(attrs,bg=PANEL);grid.pack(fill="x",pady=(12,0))
        for index,name in enumerate(ATTRIBUTES):
            cell=tk.Frame(grid,bg=PANEL);cell.grid(row=index//2,column=index%2,sticky="ew",padx=(0,16),pady=6)
            grid.grid_columnconfigure(index%2,weight=1)
            tk.Label(cell,text=name.upper(),bg=PANEL,fg=MUTED,font=(FONT,8,"bold")).pack(anchor="w")
            bar=ttk.Progressbar(cell,maximum=999,style="Eclipse.Horizontal.TProgressbar");bar.pack(fill="x",pady=(5,0))
            self.attribute_bars[name]=bar
    def _build_quests(self):
        p=self._page("quests");self._heading(p,"Daily directives","Choose what matters today. Record a directive only after you have actually done it.")
        self.quest_tree=self._tree(p,("title","category","xp","state"),("DIRECTIVE","ATTRIBUTE","REWARD","STATUS"),(500,150,100,140),12)
        bar=tk.Frame(p,bg=BG);bar.pack(fill="x");self._button(bar,"COMPLETE SELECTED",self.complete_quest,"success").pack(side="left")
        self._button(bar,"ADD CUSTOM DIRECTIVE",self.add_quest).pack(side="left",padx=8);self._button(bar,"REMOVE SELECTED",self.remove_quest,"danger").pack(side="right")
    def _build_goals(self):
        p=self._page("goals");self._heading(p,"Long-range objectives","The System analyses momentum; you confirm a goal only when it is genuinely finished.")
        self.goal_tree=self._tree(p,("state","created"),("STATUS","CREATED"),(160,200),12,show="tree headings")
        self.goal_tree.heading("#0",text="OBJECTIVE");self.goal_tree.column("#0",width=560,anchor="w")
        bar=tk.Frame(p,bg=BG);bar.pack(fill="x");self._button(bar,"ADD OBJECTIVE",self.add_goal).pack(side="left")
        self._button(bar,"CONFIRM GOAL COMPLETE",self.complete_goal,"success").pack(side="left",padx=8);self._button(bar,"REMOVE ACTIVE",self.remove_goal,"danger").pack(side="right")
    def _build_habits(self):
        p=self._page("habits");self._heading(p,"Habit architecture","Track consistency without streak pressure. A missed day never erases earlier progress.")
        self.habit_tree=self._tree(p,("title","today","total"),("HABIT","TODAY","TOTAL CHECK-INS"),(500,180,180),12)
        bar=tk.Frame(p,bg=BG);bar.pack(fill="x");self._button(bar,"ADD HABIT",self.add_habit).pack(side="left")
        self._button(bar,"CHECK IN TODAY",self.complete_habit,"success").pack(side="left",padx=8);self._button(bar,"ARCHIVE HABIT",self.archive_habit,"danger").pack(side="right")
    def _build_focus(self):
        p=self._page("focus");self._heading(p,"Focus room","A calm timer for intentional work. It records elapsed sessions, not what you did on screen.")
        c=self._card(p,"CURRENT SESSION","Choose a duration that fits the task and your energy.");c.pack(fill="x",pady=8)
        self.timer_display=self._label(c,"25:00",48,ACCENT,True,PANEL);self.timer_display.pack(pady=(15,8))
        self.timer_hint=self._label(c,"Ready when you are.",9,MUTED,PANEL);self.timer_hint.pack(pady=(0,12))
        row=tk.Frame(c,bg=PANEL);row.pack(pady=5);self._button(row,"START SESSION",self.start_timer,"success").pack(side="left",padx=4)
        self._button(row,"PAUSE",self.pause_timer,"quiet").pack(side="left",padx=4);self._button(row,"RESET",self.reset_timer,"danger").pack(side="left",padx=4)
        controls=tk.Frame(c,bg=PANEL);controls.pack(pady=(15,5));self._label(controls,"SESSION LENGTH",8,MUTED,True,PANEL).pack(side="left",padx=8)
        self.timer_choice=tk.StringVar(value="25 minutes");combo=ttk.Combobox(controls,textvariable=self.timer_choice,values=["5 minutes","15 minutes","25 minutes","45 minutes","60 minutes"],state="readonly",width=15)
        combo.pack(side="left");combo.bind("<<ComboboxSelected>>",lambda _e:self.reset_timer())
        recent=self._card(p,"RECENT FOCUS RECORDS","Only completed sessions appear here.");recent.pack(fill="both",expand=True,pady=8)
        self.focus_recent=self._text(recent,8);self.focus_recent.pack(fill="both",expand=True,pady=(8,0));self.focus_recent.configure(state="disabled")
    def _build_growth(self):
        p=self._page("growth");self._heading(p,"System intelligence","Patterns come from your check-ins and in-app records—not hidden surveillance.")
        self.growth_text=self._text(p,24);self.growth_text.pack(fill="both",expand=True);self.growth_text.configure(state="disabled")
    def _build_story(self):
        p=self._page("story");self._heading(p,"The unknown archive","Original story fragments unlock as your recorded journey develops.")
        self.story_text=self._text(p,24);self.story_text.pack(fill="both",expand=True);self.story_text.configure(state="disabled")
    def _build_journal(self):
        p=self._page("journal");self._heading(p,"Daily journal","Private reflection saved locally. Journal text is excluded from analysis by default.")
        self.journal_text=self._text(p,18);self.journal_text.pack(fill="both",expand=True);self._button(p,"SAVE TODAY'S REFLECTION",self.save_reflection,"success").pack(anchor="e",pady=12)
    def _build_history(self):
        p=self._page("history");self._heading(p,"Activity log","Transparent timeline of ECLIPSE events. No keystrokes, screenshots or app usage are collected.")
        self.history_text=self._text(p,24);self.history_text.pack(fill="both",expand=True);self.history_text.configure(state="disabled")
    def _build_settings(self):
        p=self._page("settings");self._heading(p,"System configuration","Tune startup, daily analysis and privacy. Preferences stay on this PC.")
        data=self._card(p,"LOCAL DATA CORE",str(self.engine.db_path));data.pack(fill="x",pady=(0,12));self._button(data,"OPEN DATA FOLDER",self.open_data_folder,"quiet").pack(anchor="w",pady=(10,0))
        startup=self._card(p,"WINDOWS STARTUP","Launch ECLIPSE automatically when you sign in to Windows.");startup.pack(fill="x",pady=6)
        self.auto_start_var=tk.IntVar(value=int(self.engine.get_setting("auto_start","0")))
        tk.Checkbutton(startup,text="Start ECLIPSE when I sign in to this PC",variable=self.auto_start_var,command=self.toggle_auto_start,bg=PANEL,fg=TEXT,selectcolor=PANEL2,activebackground=PANEL,activeforeground=TEXT,font=(FONT,9)).pack(anchor="w",pady=4)
        daily=self._card(p,"DAILY INTELLIGENCE","Choose what the System asks and analyses.");daily.pack(fill="x",pady=6)
        self.auto_checkin_var=tk.IntVar(value=int(self.engine.get_setting("auto_checkin","1")))
        tk.Checkbutton(daily,text="Ask for a daily check-in when ECLIPSE opens (once per day)",variable=self.auto_checkin_var,command=lambda:self._save_setting("auto_checkin",self.auto_checkin_var.get()),bg=PANEL,fg=TEXT,selectcolor=PANEL2,activebackground=PANEL,activeforeground=TEXT,font=(FONT,9)).pack(anchor="w",pady=3)
        row=tk.Frame(daily,bg=PANEL);row.pack(anchor="w",pady=5);self._label(row,"ANALYSIS WINDOW",8,MUTED,True,PANEL).pack(side="left",padx=(0,10))
        self.analysis_window=tk.StringVar(value=self.engine.get_setting("analysis_window","7"))
        window=ttk.Combobox(row,textvariable=self.analysis_window,values=["7","14","30"],state="readonly",width=8);window.pack(side="left")
        window.bind("<<ComboboxSelected>>",lambda _e:self._save_setting("analysis_window",self.analysis_window.get()))
        self.include_focus_var=tk.IntVar(value=int(self.engine.get_setting("include_focus","1")))
        tk.Checkbutton(daily,text="Include completed focus sessions in analysis",variable=self.include_focus_var,command=lambda:self._save_setting("include_focus",self.include_focus_var.get()),bg=PANEL,fg=TEXT,selectcolor=PANEL2,activebackground=PANEL,activeforeground=TEXT,font=(FONT,9)).pack(anchor="w",pady=3)
        self.include_habits_var=tk.IntVar(value=int(self.engine.get_setting("include_habits","1")))
        tk.Checkbutton(daily,text="Include habit check-ins in analysis",variable=self.include_habits_var,command=lambda:self._save_setting("include_habits",self.include_habits_var.get()),bg=PANEL,fg=TEXT,selectcolor=PANEL2,activebackground=PANEL,activeforeground=TEXT,font=(FONT,9)).pack(anchor="w",pady=3)
        self.include_checkins_var=tk.IntVar(value=int(self.engine.get_setting("include_checkins","1")))
        tk.Checkbutton(daily,text="Include daily pulse ratings in analysis",variable=self.include_checkins_var,command=lambda:self._save_setting("include_checkins",self.include_checkins_var.get()),bg=PANEL,fg=TEXT,selectcolor=PANEL2,activebackground=PANEL,activeforeground=TEXT,font=(FONT,9)).pack(anchor="w",pady=3)
        self.include_goals_var=tk.IntVar(value=int(self.engine.get_setting("include_goals","1")))
        tk.Checkbutton(daily,text="Include objective completions in analysis",variable=self.include_goals_var,command=lambda:self._save_setting("include_goals",self.include_goals_var.get()),bg=PANEL,fg=TEXT,selectcolor=PANEL2,activebackground=PANEL,activeforeground=TEXT,font=(FONT,9)).pack(anchor="w",pady=3)
        tk.Label(daily,text="Journal contents stay private and are never analysed.",bg=PANEL,fg=GOLD,font=(FONT,8)).pack(anchor="w",pady=(5,0))
        data=self._card(p,"BACKUP & MAINTENANCE","Protect your progress before moving or restoring data.");data.pack(fill="x",pady=6)
        row=tk.Frame(data,bg=PANEL);row.pack(anchor="w",pady=(10,0))
        for label,cmd,kind in [("BACK UP DATABASE",self.backup_db,"quiet"),("EXPORT JSON",self.export_json,"quiet"),("RESTORE JSON",self.import_json,"danger"),("SYSTEM CHECK",self.system_check,"success"),("PLAYER NAME",self.rename_player,"quiet")]:
            self._button(row,label,cmd,kind).pack(side="left",padx=(0,7))
        self.check_text=self._text(p,6);self.check_text.pack(fill="both",expand=True,pady=(10,0));self.check_text.insert("1.0","System diagnostics have not been run in this session.");self.check_text.configure(state="disabled")
    def show_page(self,key):
        if key not in self.pages:return
        for page in self.page_containers.values():page.pack_forget()
        self._active_scroll_canvas=self.page_canvases[key]
        self.page_containers[key].pack(fill="both",expand=True)
        self.page_title.configure(text=dict((k,label.title()) for label,k,_ in self.NAV).get(key,"ECLIPSE"))
        for k,b in self.nav_buttons.items():b.configure(bg=PANEL2 if k==key else SIDE,fg=ACCENT if k==key else MUTED)
        if key=="settings":
            self.auto_start_var.set(int(self.engine.get_setting("auto_start","0")))
            self.auto_checkin_var.set(int(self.engine.get_setting("auto_checkin","1")))
            self.include_focus_var.set(int(self.engine.get_setting("include_focus","1")))
            self.include_habits_var.set(int(self.engine.get_setting("include_habits","1")))
            self.include_checkins_var.set(int(self.engine.get_setting("include_checkins","1")))
            self.include_goals_var.set(int(self.engine.get_setting("include_goals","1")))
    def refresh_all(self):
        snap=self.brain.snapshot();player=snap["player"];days=int(self.engine.get_setting("analysis_window","7"));a=self.engine.analytics_snapshot(days)
        self.player_name.configure(text=player["name"].upper());self.player_rank.configure(text=f"RANK {player['rank']}  ·  LEVEL {player['level']}")
        self.hero_greeting.configure(text=f"WELCOME BACK, {player['name'].upper()}");self.level_line.configure(text=f"LEVEL {player['level']}  ·  RANK {player['rank']}")
        self.xp_line.configure(text=f"{player['level_xp']} / {player['next_xp']} XP TO NEXT LEVEL");self.level_bar["value"]=player["level_xp"]/player["next_xp"]*100
        self.metric_labels["xp"].configure(text=f"{player['xp']:,}");self.metric_labels["quests"].configure(text=str(a["quest_count"]))
        for name,value in player["attributes"].items():
            if name in self.attribute_bars:self.attribute_bars[name]["value"]=value
        self.metric_labels["habits"].configure(text=str(a["habit_count"] if self.engine.get_setting("include_habits","1")=="1" else 0));self.metric_labels["focus"].configure(text=f"{a['focus_minutes'] if self.engine.get_setting('include_focus','1')=='1' else 0}m")
        pulse=self.engine.daily_checkin()
        if pulse:
            self.checkin_state.configure(text="TODAY'S PULSE RECORDED",fg=GREEN)
            self.checkin_detail.configure(text=f"Mood {pulse['mood']}/5  ·  Energy {pulse['energy']}/5  ·  Focus {pulse['focus']}/5\nPriority: {pulse['priority'] or 'Not set'}")
        else:
            self.checkin_state.configure(text="NO CHECK-IN RECORDED TODAY",fg=GOLD);self.checkin_detail.configure(text="A quick pulse gives the System useful context. You can skip it.")
        self._set_text(self.daily_insight,self.brain.daily_report(days,self.engine.get_setting('include_focus','1')=='1',self.engine.get_setting('include_habits','1')=='1',self.engine.get_setting('include_checkins','1')=='1',self.engine.get_setting('include_goals','1')=='1'))
        self._set_text(self.growth_text,self.brain.full_report(self.engine.get_setting("include_focus","1")=="1",self.engine.get_setting("include_habits","1")=="1",days,self.engine.get_setting("include_checkins","1")=="1",self.engine.get_setting("include_goals","1")=="1"))
        for tree in (self.quest_tree,self.goal_tree,self.habit_tree):
            for item in tree.get_children():tree.delete(item)
        for q in self.engine.quests():self.quest_tree.insert("","end",iid=str(q["id"]),values=(q["title"],q["category"],f"+{q['xp']} XP","RECORDED" if q["completed"] else "AVAILABLE"))
        for g in self.engine.goals():self.goal_tree.insert("","end",iid=str(g["id"]),text=g["title"],values=("COMPLETED" if g["completed"] else "ACTIVE",g["created_at"][:10]))
        for h in self.engine.habits():self.habit_tree.insert("","end",iid=str(h["id"]),values=(h["title"],"DONE" if h["done_today"] else "NOT YET",h["total_completions"]))
        self._set_text(self.story_text,"\n\n".join(f"{c['title']}  [{'UNLOCKED' if c['unlocked'] else 'LOCKED · '+str(c['required_records'])+' records required'}]\n{c['body'] if c['unlocked'] else 'This archive fragment has not yet been released.'}" for c in snap["chapters"]))
        self._set_text(self.history_text,"\n\n".join(f"[{e['created_at']}]  {e['kind'].upper()}\n{e['detail']}" for e in self.engine.recent_events(150)) or "No events recorded yet.")
        self.journal_text.delete("1.0","end");self.journal_text.insert("1.0",self.engine.reflection())
        self._set_text(self.focus_recent,"\n".join(f"{s['day']}  ·  {s['minutes']} minutes  ·  {'COMPLETED' if s['completed'] else 'STOPPED'}" for s in self.engine.recent_focus_sessions(12)) or "No focus sessions recorded yet.")
        self.date_label.configure(text=date.today().strftime("%A  ·  %d %B %Y"))
    def _maybe_daily_checkin(self):
        today=date.today().isoformat()
        if (self.engine.daily_checkin() is None and self.engine.get_setting("auto_checkin","1")=="1"
                and self.engine.get_setting("last_checkin_prompt_date","")!=today):
            self.engine.set_setting("last_checkin_prompt_date",today)
            self.open_daily_checkin()
    def open_daily_checkin(self):
        self.engine.set_setting("last_checkin_prompt_date",date.today().isoformat())
        old=self.engine.daily_checkin();win=tk.Toplevel(self.root);win.title("ECLIPSE | Daily pulse");win.configure(bg=BG);win.resizable(False,False);win.transient(self.root);win.grab_set();win.geometry("540x610")
        body=tk.Frame(win,bg=PANEL,padx=24,pady=22);body.pack(fill="both",expand=True,padx=14,pady=14)
        self._label(body,"DAILY SYSTEM PULSE",9,ACCENT,True,PANEL).pack(anchor="w");self._label(body,"How is today going?",20,TEXT,True,PANEL).pack(anchor="w",pady=(6,3))
        self._label(body,"A quick snapshot helps ECLIPSE give useful, grounded insights.",8,MUTED,PANEL,wraplength=450,justify="left").pack(anchor="w",pady=(0,15))
        scales={}
        for key,label in [("mood","MOOD"),("energy","ENERGY"),("focus","FOCUS")]:
            row=tk.Frame(body,bg=PANEL);row.pack(fill="x",pady=5);tk.Label(row,text=label,bg=PANEL,fg=MUTED,font=(FONT,8,"bold"),width=10,anchor="w").pack(side="left")
            var=tk.IntVar(value=old[key] if old else 3);tk.Scale(row,from_=1,to=5,orient="horizontal",variable=var,bg=PANEL,fg=TEXT,troughcolor=PANEL2,highlightthickness=0,activebackground=ACCENT,length=300).pack(side="left",fill="x",expand=True);scales[key]=var
        fields={}
        for key,label in [("win","ONE THING THAT WENT WELL"),("challenge","WHAT FELT DIFFICULT?"),("priority","ONE PRIORITY FOR TODAY")]:
            tk.Label(body,text=label,bg=PANEL,fg=MUTED,font=(FONT,7,"bold")).pack(anchor="w",pady=(8,2))
            entry=tk.Entry(body,bg=PANEL2,fg=TEXT,insertbackground=TEXT,relief="flat",font=(FONT,9));entry.pack(fill="x",ipady=7)
            if old:entry.insert(0,old[key] or "")
            fields[key]=entry
        buttons=tk.Frame(body,bg=PANEL);buttons.pack(fill="x",pady=(18,0))
        def save():
            values={k:v.get() for k,v in scales.items()};values.update({k:v.get().strip() for k,v in fields.items()})
            self.engine.save_daily_checkin(**values);self.refresh_all();win.destroy()
        self._button(buttons,"SAVE TODAY'S PULSE",save,"success").pack(side="left");self._button(buttons,"SKIP FOR NOW",win.destroy,"quiet").pack(side="right")
    def _selected(self,tree):
        sel=tree.selection()
        if not sel:messagebox.showinfo("ECLIPSE","Select an item first.",parent=self.root);return None
        return int(sel[0])
    def complete_quest(self):
        i=self._selected(self.quest_tree)
        if i is not None:
            if self.engine.complete_quest(i):self.refresh_all();messagebox.showinfo("ECLIPSE","Record accepted. Progress updated.",parent=self.root)
            else:messagebox.showinfo("ECLIPSE","Already recorded or unavailable.",parent=self.root)
    def add_quest(self):
        title=simpledialog.askstring("Custom directive","What task do you want to add?",parent=self.root)
        if not title:return
        cat=simpledialog.askstring("Attribute","Choose one: "+", ".join(ATTRIBUTES),initialvalue="Focus",parent=self.root)
        if not cat:return
        cat=next((a for a in ATTRIBUTES if a.lower()==cat.strip().lower()),None)
        if not cat:messagebox.showerror("ECLIPSE","Unknown attribute.",parent=self.root);return
        xp=simpledialog.askinteger("Reward","Choose XP reward (5–50).",initialvalue=20,minvalue=5,maxvalue=50,parent=self.root)
        if xp is not None:self.engine.add_custom_quest(title,cat,xp);self.refresh_all()
    def remove_quest(self):
        i=self._selected(self.quest_tree)
        if i is not None and messagebox.askyesno("Remove directive","Remove this uncompleted directive?",parent=self.root):self.engine.delete_quest(i);self.refresh_all()
    def add_goal(self):
        title=simpledialog.askstring("New objective","What meaningful objective do you want to work toward?",parent=self.root)
        if title:self.engine.add_goal(title);self.refresh_all()
    def complete_goal(self):
        i=self._selected(self.goal_tree)
        if i is not None and messagebox.askyesno("Confirm objective","Have you genuinely completed this objective?",parent=self.root):
            if self.engine.complete_goal(i):self.refresh_all();messagebox.showinfo("ECLIPSE","Objective completion recorded. +30 XP",parent=self.root)
    def remove_goal(self):
        i=self._selected(self.goal_tree)
        if i is not None and messagebox.askyesno("Remove objective","Remove this active objective?",parent=self.root):self.engine.delete_goal(i);self.refresh_all()
    def add_habit(self):
        title=simpledialog.askstring("New habit","Name a small habit you want to track.",parent=self.root)
        if title:self.engine.add_habit(title);self.refresh_all()
    def complete_habit(self):
        i=self._selected(self.habit_tree)
        if i is not None:
            if self.engine.complete_habit(i):self.refresh_all()
            else:messagebox.showinfo("ECLIPSE","This habit already has a check-in today.",parent=self.root)
    def archive_habit(self):
        i=self._selected(self.habit_tree)
        if i is not None and messagebox.askyesno("Archive habit","Hide this habit? Past check-ins stay saved.",parent=self.root):self.engine.archive_habit(i);self.refresh_all()
    def _show_timer(self):self.timer_display.configure(text=f"{self.timer_remaining//60:02d}:{self.timer_remaining%60:02d}")
    def _timer_tick(self):
        if not self.timer_running:return
        self.timer_elapsed+=1;self.timer_remaining-=1;self._show_timer()
        if self.timer_remaining<=0:
            self.timer_running=False;self.timer_job=None;mins=int(self.timer_choice.get().split()[0]);self.engine.record_focus_session(mins,True);self.timer_elapsed=0
            self.timer_hint.configure(text="Session complete. Take a break if you need one.");self.refresh_all();self.root.bell()
            messagebox.showinfo("Focus Room","Focus session completed and recorded.",parent=self.root);return
        self.timer_job=self.root.after(1000,self._timer_tick)
    def start_timer(self):
        if self.timer_running:return
        if self.timer_remaining<=0:
            self.timer_remaining=int(self.timer_choice.get().split()[0])*60;self.timer_elapsed=0;self._show_timer()
        self.timer_running=True;self.timer_hint.configure(text="Timer running locally. Pause whenever you need.");self.timer_job=self.root.after(1000,self._timer_tick)
    def pause_timer(self):
        if self.timer_running:
            self.timer_running=False
            if self.timer_job:self.root.after_cancel(self.timer_job);self.timer_job=None
            self.timer_hint.configure(text="Paused. Continue when you are ready.")
    def _record_interrupted_focus(self):
        minutes=self.timer_elapsed//60
        if minutes>0:self.engine.record_focus_session(minutes,False)
        self.timer_elapsed=0
    def reset_timer(self):
        self.pause_timer();self._record_interrupted_focus();self.timer_remaining=int(self.timer_choice.get().split()[0])*60;self._show_timer();self.timer_hint.configure(text="Timer reset. Choose a comfortable pace.");self.refresh_all()
    def save_reflection(self):
        self.engine.save_reflection(self.journal_text.get("1.0","end").strip());self.refresh_all();messagebox.showinfo("Journal","Reflection saved locally.",parent=self.root)
    def _save_setting(self,key,value):
        self.engine.set_setting(key,str(value));self.status.configure(text=f"SETTING SAVED  ·  {key.replace('_',' ').upper()}");self.refresh_all()
    def toggle_auto_start(self):
        enabled=bool(self.auto_start_var.get())
        try:self._set_windows_startup(enabled);self.engine.set_setting("auto_start","1" if enabled else "0");self.status.configure(text="WINDOWS STARTUP ENABLED" if enabled else "WINDOWS STARTUP DISABLED")
        except Exception as exc:self.auto_start_var.set(0 if enabled else 1);messagebox.showerror("Startup setting",str(exc),parent=self.root)
    def _set_windows_startup(self,enabled):
        if sys.platform!="win32":raise RuntimeError("Automatic sign-in launch is currently supported on Windows only.")
        startup=Path(os.environ.get("APPDATA",""))/"Microsoft"/"Windows"/"Start Menu"/"Programs"/"Startup";startup.mkdir(parents=True,exist_ok=True);vbs=startup/"ECLIPSE_STARTUP.vbs"
        if not enabled:vbs.unlink(missing_ok=True);return
        pythonw=Path(sys.executable).with_name("pythonw.exe")
        if not pythonw.exists():raise RuntimeError("pythonw.exe was not found beside this Python installation.")
        project=Path(__file__).resolve().parent.parent
        qproj=str(project).replace('"','""');qpython=str(pythonw).replace('"','""')
        vbs.write_text('Set shell = CreateObject("WScript.Shell")\n'+f'shell.CurrentDirectory = "{qproj}"\n'+f'shell.Run """{qpython}"" -m eclipse", 0, False\n',encoding="utf-8")
    def rename_player(self):
        name=simpledialog.askstring("Player profile","Choose your player name:",initialvalue=self.engine.player()["name"],parent=self.root)
        if name:self.engine.rename_player(name);self.refresh_all()
    def backup_db(self):
        path=filedialog.asksaveasfilename(parent=self.root,title="Save ECLIPSE database backup",defaultextension=".db",initialfile=f"eclipse_backup_{datetime.now():%Y%m%d_%H%M}.db",filetypes=[("SQLite database","*.db")])
        if path:self.engine.backup(path);messagebox.showinfo("Backup",f"Backup saved:\n{path}",parent=self.root)
    def export_json(self):
        path=filedialog.asksaveasfilename(parent=self.root,title="Export ECLIPSE progress",defaultextension=".json",initialfile="eclipse_export.json",filetypes=[("JSON backup","*.json")])
        if path:self.engine.export_json(path);messagebox.showinfo("Export complete",f"Portable backup saved:\n{path}",parent=self.root)
    def import_json(self):
        path=filedialog.askopenfilename(parent=self.root,title="Choose ECLIPSE JSON backup",filetypes=[("JSON backup","*.json")])
        if not path:return
        if not messagebox.askyesno("Restore progress","This replaces current records. Create a safety backup and continue?",parent=self.root):return
        try:
            safety=self.data_dir/f"pre_restore_{datetime.now():%Y%m%d_%H%M%S}.db";self.engine.backup(safety);self.engine.import_json(path);self.refresh_all()
            messagebox.showinfo("Restore complete",f"Progress restored. Safety backup:\n{safety}",parent=self.root)
        except Exception as exc:messagebox.showerror("Restore failed",str(exc),parent=self.root)
    def system_check(self):
        checks=[];tests=[("Database connection",lambda:self.engine.conn.execute("SELECT 1").fetchone()[0]==1),
        ("SQLite integrity",lambda:self.engine.conn.execute("PRAGMA integrity_check").fetchone()[0]=="ok"),
        ("Player profile",lambda:bool(self.engine.player()["name"])),("Daily directives",lambda:len(self.engine.quests())>=5),
        ("Daily analytics",lambda:isinstance(self.engine.analytics_snapshot(7),dict)),("Backup capability",self._test_backup)]
        for name,fn in tests:
            try:checks.append((name,bool(fn())))
            except Exception:checks.append((name,False))
        out="ECLIPSE 3.1 SYSTEM DIAGNOSTICS\n"+"="*38+"\n"+"\n".join(("PASS  " if ok else "FAIL  ")+name for name,ok in checks)
        out+=f"\n\nRESULT: {sum(ok for _,ok in checks)}/{len(checks)} checks passed.\nPython: {sys.version.split()[0]} · Platform: {sys.platform}\nTk: {self.root.tk.call('info','patchlevel')}\nDatabase: {self.engine.db_path}"
        self._set_text(self.check_text,out)
    def _test_backup(self):
        path=self.data_dir/"diagnostic_backup.db";self.engine.backup(path);valid=path.exists() and path.stat().st_size>0;path.unlink(missing_ok=True);return valid
    def open_data_folder(self):
        try:
            if sys.platform=="win32":os.startfile(self.data_dir)
            elif sys.platform=="darwin":os.system(f'open "{self.data_dir}"')
            else:os.system(f'xdg-open "{self.data_dir}"')
        except Exception as exc:messagebox.showerror("Data folder",str(exc),parent=self.root)
    def close(self):
        if self.timer_running:self.pause_timer()
        self._record_interrupted_focus()
        if self.timer_job:
            try:self.root.after_cancel(self.timer_job)
            except Exception:pass
        self.engine.close();self.root.destroy()

def main():
    root=tk.Tk();EclipseApp(root);root.mainloop()
if __name__=="__main__":main()
