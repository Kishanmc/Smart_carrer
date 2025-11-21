# llm_client.py - simple wrapper to support real LLMs or a mock for offline/demo usage.
import os
import time
import json

LLM_PROVIDER = os.environ.get('LLM_PROVIDER', 'mock')  # 'openai' or 'mock'

class LLMClient:
    def __init__(self):
        self.provider = LLM_PROVIDER.lower()
        if self.provider == 'openai':
            try:
                import openai
                self.openai = openai
                self.api_key = os.environ.get('OPENAI_API_KEY')
                if not self.api_key:
                    raise ValueError('OPENAI_API_KEY not set')
                self.openai.api_key = self.api_key
            except Exception as e:
                print('OpenAI init error:', e)
                self.provider = 'mock'

    def chat(self, prompt, max_tokens=256, temperature=0.2):
        if self.provider == 'openai':
            resp = self.openai.ChatCompletion.create(
                model='gpt-4o-mini' if hasattr(self.openai, 'ChatCompletion') else 'gpt-4o-mini',
                messages=[{'role':'user','content':prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            # adapt to API shape
            if 'choices' in resp and len(resp['choices'])>0:
                return resp['choices'][0]['message']['content']
            return str(resp)
        # Mock deterministic response for offline/demo use
        time.sleep(0.2)
        if 'generate project' in prompt.lower():
            return json.dumps([{"title":"Demo Project","description":"A small demo project."}])
        if 'extract' in prompt.lower() or 'profile' in prompt.lower():
            return "{""semester"": 3, ""interests"": ["frontend","dsa"]}"
        # default
        return "This is a mock LLM response based on: " + (prompt[:200])

# Convenience function
def get_llm():
    return LLMClient()
