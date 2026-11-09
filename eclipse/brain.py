"""Explainable, local System Intelligence for ECLIPSE."""
from collections import Counter
from .engine import ATTRIBUTES, STORY
class SystemBrain:
    def __init__(self,engine):self.engine=engine
    def snapshot(self):
        p=self.engine.player();events=self.engine.conn.execute("SELECT kind FROM events").fetchall();counts=Counter(r["kind"] for r in events);attrs=p["attributes"]
        weakest=min(ATTRIBUTES,key=lambda n:(attrs.get(n,1),n));strongest=max(ATTRIBUTES,key=lambda n:(attrs.get(n,1),n));q=counts["quest_completed"]
        advice=("Start with one small directive. The System needs a real record before it can identify patterns." if q==0 else
                "Keep recording a few different kinds of activity before drawing conclusions." if q<3 else
                f"Your most-practised recorded attribute is {strongest}. Consider a manageable activity in {weakest}.")
        achievements=[("First Signal","Complete your first directive.",q>=1),("Signal Detected","Complete three directives.",q>=3),
        ("Pattern Recognition","Complete ten directives.",q>=10),("A Chosen Destination","Complete an objective.",counts["goal_completed"]>=1),
        ("Milestone Maker","Complete five objectives.",counts["goal_completed"]>=5),("Daily Rhythm","Complete ten habit check-ins.",counts["habit_completed"]>=10)]
        skills=[("Focused Initiate","Focus"),("Knowledge Seeker","Knowledge"),("Creative Spark","Creativity"),("Resilient Return","Resilience")]
        chapters=[]
        for i,(title,body) in enumerate(STORY):
            req=(0,1,3,8,15)[i];chapters.append({"title":title,"body":body,"required_records":req,"unlocked":q>=req})
        return {"player":p,"quest_records":q,"goal_records":counts["goal_completed"],"event_count":len(events),"strongest_attribute":strongest,"weakest_attribute":weakest,
        "recommendation":advice,"achievements":[{"title":a,"description":d,"unlocked":u} for a,d,u in achievements],
        "skills":[{"title":n,"attribute":a,"value":attrs.get(a,1),"unlocked":attrs.get(a,1)>=3} for n,a in skills],"chapters":chapters}
    def daily_report(self,days=7):
        d=self.engine.analytics_snapshot(days);pulse=self.engine.daily_checkin()
        lines=[f"ANALYSIS WINDOW · LAST {d['days']} DAYS",f"{d['start']} → {d['end']}","",f"Directives completed: {d['quest_count']}",
        f"Habit check-ins: {d['habit_count']}",f"Completed focus time: {d['focus_minutes']} minutes",f"Daily pulses recorded: {d['checkin_count']}",
        f"Objectives completed: {d['goal_count']}",""]
        if pulse:
            lines += ["TODAY'S SELF-REPORTED PULSE",f"Mood {pulse['mood']}/5 · Energy {pulse['energy']}/5 · Focus {pulse['focus']}/5",
            f"Win: {pulse['win'] or 'Not recorded'}",f"Challenge: {pulse['challenge'] or 'Not recorded'}",f"Priority: {pulse['priority'] or 'Not recorded'}",""]
            if pulse["energy"]<=2 or pulse["mood"]<=2:lines.append("SYSTEM NOTE: Your check-in suggests keeping today's plan lighter and choosing one manageable priority.")
            elif pulse["focus"]>=4 and pulse["energy"]>=4:lines.append("SYSTEM NOTE: You reported strong focus and energy. Protect one focused block, then take a proper break.")
            else:lines.append("SYSTEM NOTE: Choose one clear priority. A steady, realistic plan is more useful than an overloaded one.")
        else:lines.append("No daily pulse has been recorded yet. The System will not guess how you feel.")
        if d["quest_count"]==0 and d["habit_count"]==0 and d["focus_minutes"]==0:lines += ["","SIGNAL STATUS: Not enough recent activity to identify a pattern. Start with one small action."]
        else:lines += ["","SIGNAL STATUS: Recent activity is available. Trends are descriptive, not a judgement or diagnosis."]
        lines += ["","DATA BOUNDARY: ECLIPSE uses only your check-ins and actions recorded inside the app."]
        return "\n".join(lines)
    def full_report(self,include_focus=True,include_habits=True,days=7):
        s=self.snapshot();attrs=s["player"]["attributes"]
        lines=["ECLIPSE SYSTEM INTELLIGENCE","="*36,self.daily_report(days),"","CHARACTER PROFILE",
        f"Player: {s['player']['name']}",f"Level {s['player']['level']} · Rank {s['player']['rank']} · {s['player']['xp']} total XP",
        f"Most practised recorded attribute: {s['strongest_attribute']}",f"Least practised recorded attribute: {s['weakest_attribute']}","","ATTRIBUTE MATRIX"]
        lines += [f"{k}: {v}" for k,v in attrs.items()]
        lines += ["","ACHIEVEMENTS"]+[f"{'UNLOCKED' if a['unlocked'] else 'LOCKED'} · {a['title']} — {a['description']}" for a in s["achievements"]]
        lines += ["","SKILL EVOLUTION"]+[f"{'UNLOCKED' if x['unlocked'] else 'LOCKED'} · {x['title']} ({x['attribute']} {x['value']}/3)" for x in s["skills"]]
        lines += ["","ANALYSIS OPTIONS","Focus sessions: included" if include_focus else "Focus sessions: excluded",
        "Habit check-ins: included" if include_habits else "Habit check-ins: excluded","Journal contents: always private and excluded"]
        return "\n".join(lines)
