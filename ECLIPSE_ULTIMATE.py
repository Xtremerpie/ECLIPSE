import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os, random
from datetime import datetime,date

BASE=os.path.dirname(os.path.abspath(__file__)); SAVE=os.path.join(BASE,"eclipse_save.json")
DEFAULT={"name":"PLAYER","level":1,"xp":0,"next":100,"rank":"F","coins":0,"streak":0,"done":0,
"stats":{"Knowledge":1,"Focus":1,"Discipline":1,"Creativity":1,"Courage":1,"Social":1},
"skills":[],"achievements":[],"titles":[],"inventory":[],"goals":[],"history":[],"day":""}
RANKS=[(1,"F"),(5,"E"),(10,"D"),(20,"C"),(35,"B"),(55,"A"),(80,"S"),(120,"SS")]
POOL=[
("Focus Dungeon","25 minutes of distraction-free study/work.","Focus",45),
("Knowledge Fragment","Learn one concept and explain it from memory.","Knowledge",40),
("Discipline Trial","Finish one useful task you have delayed.","Discipline",40),
("Creator Forge","Create something small: code, art, writing or a prototype.","Creativity",45),
("Courage Trial","Take one reasonable action you have been avoiding.","Courage",45),
("Social Quest","Help someone or have a positive interaction.","Social",35),
("System Journal","Write three lines: win, problem, next move.","Discipline",30),
("Deep Work Gate","Complete another focused work block.","Focus",55)]
SK=[("Focus Core","Focus",3),("Memory Forge","Knowledge",5),("Iron Discipline","Discipline",5),
("Creator Engine","Creativity",5),("Courage Node","Courage",5),("Social Link","Social",5),
("Balanced Mind","ALL",5),("Overclock","ALL",10)]
def load():
 try:
  with open(SAVE,encoding="utf8") as f:d=json.load(f)
  for k,v in DEFAULT.items():d.setdefault(k,v)
  for k,v in DEFAULT["stats"].items():d["stats"].setdefault(k,v)
  return d
 except:return json.loads(json.dumps(DEFAULT))
D=load()
def save():
 with open(SAVE,"w",encoding="utf8") as f:json.dump(D,f,indent=2)
def rank():
 r="F"
 for n,x in RANKS:
  if D["level"]>=n:r=x
 return r
def log(x):
 D["history"].append(datetime.now().strftime("%Y-%m-%d %H:%M")+"  "+x);D["history"]=D["history"][-120:];save()
def daily(force=False):
 today=str(date.today())
 if not force and D["day"]==today and D.get("quests"):return
 rng=random.Random(int(today.replace("-",""))); q=rng.sample(POOL,6)
 D["quests"]=[{"title":a,"desc":b,"stat":c,"xp":x,"done":False} for a,b,c,x in q];D["day"]=today;save()

class Eclipse:
 def __init__(self,r):
  self.r=r;self.c={"bg":"#03060b","p":"#07111b","p2":"#0a1925","line":"#17394f","cyan":"#5de8ff","w":"#eafaff","m":"#7894a8","g":"#6cffb0","gold":"#ffe27d","red":"#ff657d"}
  r.title("ECLIPSE // UNKNOWN SYSTEM // ULTIMATE");r.geometry("1240x780");r.minsize(1000,650);r.configure(bg=self.c["bg"]);r.protocol("WM_DELETE_WINDOW",self.close)
  daily();self.build();self.hud();self.scan(first=True);self.tick()
 def L(self,p,t="",s=10,c=None,b=False,bg=None):return tk.Label(p,text=t,bg=bg or self.c["bg"],fg=c or self.c["w"],font=("Consolas",s,"bold" if b else "normal"))
 def B(self,p,t,cmd):return tk.Button(p,text=t,command=cmd,bg=self.c["p2"],fg=self.c["cyan"],activebackground="#12364d",activeforeground=self.c["w"],relief="flat",font=("Consolas",9,"bold"),padx=8,pady=8)
 def build(self):
  top=tk.Frame(self.r,bg=self.c["bg"]);top.pack(fill="x",padx=20,pady=14)
  self.L(top,"E C L I P S E",25,self.c["cyan"],True).pack(side="left");self.clock=self.L(top,"",9,self.c["m"]);self.clock.pack(side="right")
  nav=tk.Frame(self.r,bg=self.c["p"],highlightbackground=self.c["line"],highlightthickness=1);nav.pack(fill="x",padx=20,pady=(0,10))
  for x in ["HUD","QUESTS","STATS","SKILLS","INVENTORY","GOALS","ARCHIVE","SYSTEM"]:self.B(nav,x,lambda z=x:self.go(z)).pack(side="left",padx=2,pady=5)
  self.main=tk.Frame(self.r,bg=self.c["bg"]);self.main.pack(fill="both",expand=True,padx=20)
 def clear(self):
  for x in self.main.winfo_children():x.destroy()
 def card(self):return tk.Frame(self.main,bg=self.c["p"],highlightbackground=self.c["line"],highlightthickness=1)
 def go(self,x):getattr(self,{"HUD":"hud","QUESTS":"quests","STATS":"stats","SKILLS":"skills","INVENTORY":"inventory","GOALS":"goals","ARCHIVE":"archive","SYSTEM":"system"}[x])()
 def hud(self):
  self.clear();a=self.card();a.pack(side="left",fill="both",expand=True,padx=(0,7));b=self.card();b.pack(side="right",fill="both",expand=True,padx=(7,0))
  self.L(a,"PLAYER HUD",11,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  self.L(a,f"{D['name']}  //  LEVEL {D['level']}     RANK {rank()}",18,self.c["w"],True).pack(anchor="w",padx=18)
  self.L(a,f"XP {D['xp']} / {D['next']}     COINS {D['coins']}     STREAK {D['streak']}",10,self.c["gold"],True).pack(anchor="w",padx=18,pady=8)
  for s,v in D["stats"].items():self.L(a,f"{s:<12} {'█'*min(v,30)} {v}",9,self.c["cyan"]).pack(anchor="w",padx=20,pady=3)
  self.L(a,f"\nMISSIONS {D['done']}   SKILLS {len(D['skills'])}   ACHIEVEMENTS {len(D['achievements'])}",9,self.c["m"]).pack(anchor="w",padx=18)
  self.L(b,"SYSTEM CORE",11,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  self.core=tk.Text(b,bg="#040a11",fg=self.c["cyan"],font=("Consolas",10),relief="flat",wrap="word");self.core.pack(fill="both",expand=True,padx=15,pady=8);self.core.config(state="disabled")
  self.B(b,"AWAKENING SCAN",self.scan).pack(fill="x",padx=15,pady=5);self.B(b,"RANDOM CHALLENGE",self.challenge).pack(fill="x",padx=15,pady=(0,12))
  self.write()
 def write(self,t=None,m=None):
  self.core.config(state="normal");self.core.delete("1.0","end");self.core.insert("end",(t+"\n\n"+m) if t else "\n".join(D["history"][-12:]));self.core.config(state="disabled")
 def quests(self):
  self.clear();c=self.card();c.pack(fill="both",expand=True);self.L(c,"QUEST BOARD // REAL WORLD",12,self.c["cyan"],True).pack(anchor="w",padx=18,pady=14)
  for i,q in enumerate(D["quests"]):
   f=tk.Frame(c,bg=self.c["p2"]);f.pack(fill="x",padx=18,pady=4);self.L(f,("✓ " if q["done"] else "◇ ")+q["title"],10,self.c["g"] if q["done"] else self.c["w"],True,self.c["p2"]).pack(anchor="w",padx=12,pady=6)
   self.L(f,q["desc"],9,self.c["m"],bg=self.c["p2"]).pack(anchor="w",padx=28);self.L(f,f"+{q['xp']} XP  •  +1 {q['stat']}",8,self.c["gold"],bg=self.c["p2"]).pack(anchor="w",padx=28,pady=3)
   if not q["done"]:self.B(f,"COMPLETE",lambda n=i:self.complete(n)).pack(anchor="e",padx=12,pady=5)
  self.B(c,"NEW DAILY SET",lambda:(daily(True),self.quests())).pack(anchor="e",padx=18,pady=10)
 def complete(self,i):
  q=D["quests"][i]
  if q["done"]:return
  q["done"]=True;gain=q["xp"];D["done"]+=1;D["coins"]+=max(5,gain//4);D["stats"][q["stat"]]+=1;old=D["level"];D["xp"]+=gain
  while D["xp"]>=D["next"]:D["xp"]-=D["next"];D["level"]+=1;D["next"]=int(D["next"]*1.22)
  D["rank"]=rank();log(f"QUEST COMPLETE: {q['title']} | +{gain} XP | +1 {q['stat']}");self.achievements()
  messagebox.showinfo("ECLIPSE","REWARD TRANSFERRED\n\n+%s XP\n+%s COINS\n+1 %s%s"%(gain,max(5,gain//4),q["stat"],f"\n\nLEVEL UP: {D['level']} / RANK {rank()}" if D["level"]>old else ""));self.hud()
 def stats(self):
  self.clear();c=self.card();c.pack(fill="both",expand=True);self.L(c,"ATTRIBUTE MATRIX",12,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  for s,v in D["stats"].items():self.L(c,f"{s:<15} {'█'*min(v,35)}  LEVEL {v}",11,self.c["w"]).pack(anchor="w",padx=25,pady=7)
  self.L(c,"\nThese are game statistics representing recorded development, not a judgment of your worth.",9,self.c["m"]).pack(anchor="w",padx=20)
 def skills(self):
  self.clear();c=self.card();c.pack(fill="both",expand=True);self.L(c,"SKILL TREE",12,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  for n,s,req in SK:
   ok=all(v>=req for v in D["stats"].values()) if s=="ALL" else D["stats"][s]>=req
   if ok and n not in D["skills"]:D["skills"].append(n);D["titles"].append(n);log("SKILL UNLOCKED: "+n)
   self.L(c,("◆ " if ok else "◇ ")+n+f"   [{s} {req}]",10,self.c["g"] if ok else self.c["m"],True).pack(anchor="w",padx=22,pady=7)
  save()
 def inventory(self):
  self.clear();c=self.card();c.pack(fill="both",expand=True);self.L(c,"INVENTORY",12,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  if not D["inventory"]:self.L(c,"Empty — special items may appear from future reward events.",10,self.c["m"]).pack(anchor="w",padx=22)
  for x in D["inventory"]:self.L(c,"◆ "+x,10,self.c["w"]).pack(anchor="w",padx=22,pady=4)
 def goals(self):
  self.clear();c=self.card();c.pack(fill="both",expand=True);self.L(c,"LONG-TERM GOALS",12,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  self.B(c,"ADD GOAL",self.addgoal).pack(anchor="w",padx=18,pady=5)
  for i,g in enumerate(D["goals"]):
   f=tk.Frame(c,bg=self.c["p2"]);f.pack(fill="x",padx=18,pady=4);self.L(f,("✓ " if g["done"] else "◇ ")+g["text"],10,self.c["g"] if g["done"] else self.c["w"],True,self.c["p2"]).pack(side="left",padx=10,pady=8)
   if not g["done"]:self.B(f,"DONE",lambda n=i:self.goal_done(n)).pack(side="right",padx=8,pady=3)
 def addgoal(self):
  x=simpledialog.askstring("Goal","Enter a meaningful goal:")
  if x and x.strip():D["goals"].append({"text":x.strip(),"done":False});log("GOAL CREATED: "+x.strip());self.goals()
 def goal_done(self,i):D["goals"][i]["done"]=True;D["coins"]+=100;D["xp"]+=75;log("GOAL COMPLETED: "+D["goals"][i]["text"]);self.achievements();self.goals()
 def archive(self):
  self.clear();c=self.card();c.pack(fill="both",expand=True);self.L(c,"ARCHIVE // MEMORY",12,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  box=tk.Text(c,bg="#040a11",fg=self.c["m"],font=("Consolas",9),relief="flat");box.pack(fill="both",expand=True,padx=15,pady=10);box.insert("end","\n".join(reversed(D["history"])));box.config(state="disabled")
 def system(self):
  self.clear();c=self.card();c.pack(fill="both",expand=True);self.L(c,"SYSTEM CONTROL",12,self.c["cyan"],True).pack(anchor="w",padx=18,pady=15)
  for x in ["LOCAL SAVE: ON","CLOUD: NOT REQUIRED","SCREEN MONITORING: OFF","PRIVATE FILE READING: OFF","PRIVATE MESSAGE READING: OFF","REAL-WORLD AUTOMATION: OFF","USER CHOICE: PRIMARY AUTHORITY"]:self.L(c,"[ "+x+" ]",10,self.c["w"]).pack(anchor="w",padx=22,pady=4)
  self.B(c,"RESET EVERYTHING",self.reset).pack(anchor="w",padx=18,pady=18)
 def achievements(self):
  tests=[("First Step",D["done"]>=1),("Awakened",D["level"]>=5),("D-Rank",D["level"]>=10),("C-Rank",D["level"]>=20),("B-Rank",D["level"]>=35),("A-Rank",D["level"]>=55),("S-Rank",D["level"]>=80),("SS-Rank",D["level"]>=120),("Ten Trials",D["done"]>=10),("Balanced",all(v>=5 for v in D["stats"].values()))]
  for n,ok in tests:
   if ok and n not in D["achievements"]:D["achievements"].append(n);D["coins"]+=25;log("ACHIEVEMENT UNLOCKED: "+n)
  save()
 def scan(self,first=False):
  pairs=[("UNKNOWN SIGNAL","The system cannot perform your growth.\nYour actions are the input."),("HIDDEN RULE","There is no final level. Only the next threshold."),("DUNGEON REPORT","The real world is the dungeon.\nAttention, learning and discipline are your resources."),("ANOMALY","Consistency compounds.\nOne useful action is small. Repeated useful actions are not.")]
  t,m=random.choice(pairs)
  if first:self.write(t,m)
  else:messagebox.showinfo("ECLIPSE // "+t,m);log("SCAN: "+t)
 def challenge(self):
  a,b,s,x=random.choice(POOL);messagebox.showinfo("RANDOM EVENT",f"{a}\n\n{b}\n\nReward: +{x} XP if you choose to complete it.\n\nOptional.")
 def reset(self):
  if messagebox.askyesno("ECLIPSE","Erase all progress?"):
   global D;D=json.loads(json.dumps(DEFAULT));daily(True);save();self.hud()
 def tick(self):
  self.clock.config(text=datetime.now().strftime("%Y-%m-%d  %H:%M:%S")+"  //  ULTIMATE");self.r.after(1000,self.tick)
 def close(self):save();self.r.destroy()

if __name__=="__main__":
    root=tk.Tk()
    Eclipse(root)
    root.mainloop()