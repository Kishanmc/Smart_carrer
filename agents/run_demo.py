# run_demo.py - quick demo driver
from agents.orchestrator import Orchestrator
import json

def demo():
    orch = Orchestrator()
    user_id = 'kishan_demo'
    text = 'I am a 3rd semester ISE student interested in frontend and DSA.'
    out = orch.handle(user_id, text)
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    demo()
