# orchestrator.py - improved orchestrator using ThreadPool for parallel agent calls
from concurrent.futures import ThreadPoolExecutor, as_completed
from .profile import ProfileAgent
from .course import CourseAgent
from .project import ProjectAgent
from .interview import InterviewAgent
from .scheduler import SchedulerAgent
from memory.vector_memory import VectorMemory
from observability.logger import logger

class Orchestrator:
    def __init__(self):
        self.memory = VectorMemory(path='memory/vector_store.json')
        self.profile_agent = ProfileAgent(self.memory)
        self.course_agent = CourseAgent(self.memory)
        self.project_agent = ProjectAgent(self.memory)
        self.interview_agent = InterviewAgent(self.memory)
        self.scheduler_agent = SchedulerAgent(self.memory)

    def handle(self, user_id, text):
        logger.info({'event': 'handle_request', 'user_id': user_id, 'text': text})
        profile = self.profile_agent.get_profile(user_id, text)
        # parallel: course and project suggestions
        results = {}
        with ThreadPoolExecutor(max_workers=4) as ex:
            futures = {
                ex.submit(self.course_agent.recommend, profile): 'courses',
                ex.submit(self.project_agent.generate, profile): 'projects',
                ex.submit(self.interview_agent.generate, profile): 'interview'
            }
            for fut in as_completed(futures):
                name = futures[fut]
                try:
                    results[name] = fut.result()
                except Exception as e:
                    logger.error({'event':'agent_error','agent':name,'error':str(e)})
                    results[name] = []

        # sequential scheduling uses results
        plan = self.scheduler_agent.create_schedule(profile, results.get('courses', []), results.get('projects', []))
        # persist profile + plan to memory
        self.memory.add_document(user_id, str({'profile': profile, 'plan': plan}), metadata={'type':'user_profile'})
        out = {'profile': profile, 'courses': results.get('courses', []), 'projects': results.get('projects', []), 'interview': results.get('interview', []), 'plan': plan}
        logger.info({'event':'response_ready','user_id':user_id})
        return out
