# scheduler.py - creates a 7-day personalized plan combining courses and projects
from datetime import date, timedelta
from observability.logger import logger

class SchedulerAgent:
    def __init__(self, memory):
        self.memory = memory

    def create_schedule(self, profile, courses, projects):
        logger.info({'event':'schedule_start','user_interests':profile.get('interests',[]) })
        plan = []
        today = date.today()
        # distribute focus across interests
        items = []
        for c in courses:
            items.append({'type':'course','title':c.get('title',c.get('snippet','Course'))})
        for p in projects:
            items.append({'type':'project','title':p.get('title')})
        if not items:
            items = [{'type':'course','title':'General CS Basics'}]
        for i in range(7):
            day = today + timedelta(days=i)
            item = items[i % len(items)]
            plan.append({'date':str(day),'task':f"{item['type'].title()}: {item['title']} - 1h"})
        logger.info({'event':'schedule_end','days':len(plan)})
        return plan
