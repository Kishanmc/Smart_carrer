# evaluation/evaluate.py - basic tests and scoring metrics
from agents.orchestrator import Orchestrator
import json, statistics

cases = [
    ('user_a','3rd sem ISE, frontend and dsa'),
    ('user_b','I want to become a backend engineer, interested in db and os'),
    ('user_c','ml and ai enthusiast, love data')
]

def score(resp):
    # simple scoring: presence of courses, projects, plan
    s = 0
    if resp.get('courses'): s += 1
    if resp.get('projects'): s += 1
    if resp.get('plan') and len(resp['plan'])==7: s += 1
    return s

def run():
    orch = Orchestrator()
    results = []
    for uid, txt in cases:
        out = orch.handle(uid, txt)
        sc = score(out)
        results.append({'user':uid, 'score':sc, 'out':out})
        print(uid, 'score', sc)
    print('Average score', statistics.mean([r['score'] for r in results]))

if __name__ == '__main__':
    run()
