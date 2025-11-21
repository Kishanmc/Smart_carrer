# profile.py - extracts structured profile using LLM and heuristics
from .llm_client import get_llm
from observability.logger import logger

class ProfileAgent:
    def __init__(self, memory):
        self.memory = memory
        self.llm = get_llm()

    def _heuristic_extract(self, text):
        profile = {}
        textl = text.lower()
        if 'semester' in textl:
            # naive extraction
            for token in textl.split():
                if token.endswith('th') or token.endswith('rd') or token.endswith('st') or token.endswith('nd'):
                    try:
                        num = int(token.replace('th','').replace('rd','').replace('st','').replace('nd',''))
                        profile['semester'] = num
                        break
                    except:
                        pass
        # keywords
        interests = []
        for k in ['frontend','backend','dsa','ml','ai','web','db','os']:
            if k in textl:
                interests.append(k)
        profile['interests'] = interests
        return profile

    def get_profile(self, user_id, text):
        logger.info({'event':'profile_extract_start','user_id':user_id})
        # Check memory for existing profile
        existing = None
        docs = self.memory.query(text=f'user:{user_id}', top_k=3)
        if docs:
            for d in docs:
                if d.get('metadata',{}).get('type')=='user_profile':
                    existing = d['text']
                    break
        # Use LLM to refine if available
        try:
            prompt = f"""Extract a JSON profile from the following user description. Return only JSON.
User: {text}
Fields: semester (int), interests (list of strings), goals (optional list)"""
            resp = self.llm.chat(prompt, max_tokens=200)
            # try to parse JSON out
            import json
            parsed = json.loads(resp)
            profile = parsed
        except Exception as e:
            profile = self._heuristic_extract(text)
        # merge with existing
        if existing:
            try:
                import ast, json
                prev = ast.literal_eval(existing)
                prev.update(profile)
                profile = prev
            except:
                pass
        logger.info({'event':'profile_extract_end','user_id':user_id,'profile':profile})
        return profile
