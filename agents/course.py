# course.py - recommends courses from multiple sources (mocked + search)
from tools.search_tool import search
from observability.logger import logger

class CourseAgent:
    def __init__(self, memory):
        self.memory = memory

    def recommend(self, profile, top_k=5):
        logger.info({'event':'course_recommend_start','interests':profile.get('interests',[]) })
        recs = []
        for it in profile.get('interests',[]):
            if it=='frontend':
                recs.append({'title':'Frontend Roadmap', 'source':'Kaggle/YouTube', 'url':'https://example.com/frontend'})
            if it=='dsa':
                recs.append({'title':'Data Structures (NPTEL)', 'source':'NPTEL', 'url':'https://example.com/dsa'})
            if it=='ml':
                recs.append({'title':'Intro to ML (Coursera)', 'source':'Coursera', 'url':'https://example.com/ml'})
        # Use search tool for supplementary hits
        hits = search(' '.join(profile.get('interests',[]))) if profile.get('interests') else search('computer science basics')
        recs += hits
        logger.info({'event':'course_recommend_end','count':len(recs)})
        return recs[:top_k]
