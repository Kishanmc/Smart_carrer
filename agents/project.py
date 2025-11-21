# project.py - generates personalized project ideas using LLM fallback to heuristics
from .llm_client import get_llm
from tools.github_tool import create_template
from observability.logger import logger

class ProjectAgent:
    def __init__(self, memory):
        self.memory = memory
        self.llm = get_llm()

    def generate(self, profile, n=3):
        logger.info({'event':'project_gen_start','interests':profile.get('interests',[]) })
        interests = profile.get('interests',[])
        projects = []
        try:
            prompt = f"""Generate {n} project ideas (title + short description) for a student with interests: {interests}. Return as JSON list."""
            resp = self.llm.chat(prompt, max_tokens=400)
            import json
            parsed = json.loads(resp)
            for p in parsed:
                p['github_template'] = create_template(p.get('title','project'))
            projects = parsed
        except Exception as e:
            # heuristic fallback
            if 'frontend' in interests:
                projects.append({'title':'Portfolio Website','description':'React + Tailwind portfolio','github_template':create_template('Portfolio Website')})
            if 'dsa' in interests:
                projects.append({'title':'DSA Visualizer','description':'Visualize sorting algorithms','github_template':create_template('DSA Visualizer')})
        logger.info({'event':'project_gen_end','count':len(projects)})
        return projects
