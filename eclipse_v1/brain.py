"""Explainable local insights based only on records entered in ECLIPSE."""
from collections import Counter
from .engine import ATTRIBUTES, STORY
class SystemBrain:
 def __init__(self,engine):self.engine=engine
 def snapshot(self):
  p=self.engine.player();events=self.engine.conn.execute('SELECT kind FROM events').fetchall();counts=Counter(r['kind'] for r in events);attrs=p['attributes']
  weakest=min(ATTRIBUTES,key=lambda n:(attrs.get(n,1),n));strongest=max(ATTRIBUTES,key=lambda n:(attrs.get(n,1),n));q=counts['quest_completed']
  advice=('Start with one small directive. The System needs a real record before it can identify patterns.' if q==0 else 'Try a few different kinds of activities before drawing conclusions.' if q<3 else f'Consider a manageable activity in {weakest}; your most-practised recorded attribute is {strongest}.')
  achievements=[('First Signal','Complete your first directive.',q>=1),('Signal Detected','Complete three directives.',q>=3),('Pattern Recognition','Complete ten directives.',q>=10),('A Chosen Destination','Complete an objective.',counts['goal_completed']>=1),('Milestone Maker','Complete five objectives.',counts['goal_completed']>=5),('Daily Rhythm','Complete ten habit check-ins.',counts['habit_completed']>=10)]
  skills=[('Focused Initiate','Focus'),('Knowledge Seeker','Knowledge'),('Creative Spark','Creativity'),('Resilient Return','Resilience')]
  chapters=[]
  for i,(title,body) in enumerate(STORY):
   req=(0,1,3,8,15)[i];chapters.append({'title':title,'body':body,'required_records':req,'unlocked':q>=req})
  return {'player':p,'quest_records':q,'goal_records':counts['goal_completed'],'event_count':len(events),'strongest_attribute':strongest,'weakest_attribute':weakest,'recommendation':advice,'achievements':[{'title':a,'description':d,'unlocked':u} for a,d,u in achievements],'skills':[{'title':n,'attribute':a,'value':attrs.get(a,1),'unlocked':attrs.get(a,1)>=3} for n,a in skills],'chapters':chapters}
