# interview.py - simple interview question generator and scoring stub
from .llm_client import get_llm
from observability.logger import logger

class InterviewAgent:
    def __init__(self, memory):
        self.memory = memory
        self.llm = get_llm()

    def generate(self, profile, n=5):
        logger.info({'event':'interview_gen_start','interests':profile.get('interests',[])})
        q = []
        interests = profile.get('interests',[])
        # heuristic questions
        if 'dsa' in interests:
            q += ['Explain time complexity of merge sort.','How does a hash table handle collisions?']
        if 'frontend' in interests:
            q += ['Explain React component lifecycle.','How would you optimize a slow web page?']
        # try LLM to expand
        try:
            prompt = f"""Create {n} mock interview questions for a student with interests {interests}. Return as JSON list."""
            resp = self.llm.chat(prompt, max_tokens=300)
            import json
            parsed = json.loads(resp)
            q = parsed
        except Exception as e:
            pass
        logger.info({'event':'interview_gen_end','count':len(q)})
        return q
