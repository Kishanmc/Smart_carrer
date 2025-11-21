# Smart Career & Learning Advisor — Advanced (Option C)

**Team:** KNSH Partners (Kishan MC, Supriya, Harshal, Nikitha Shenoy)

This is an advanced, full AI-powered version of the Smart Career & Learning Advisor for the Kaggle Agents Intensive capstone. Features:

- Modular multi-agent architecture (Orchestrator + Profile, Course, Project, Interview, Scheduler, Observability)
- LLM client wrapper supporting OpenAI/Gemini (configurable) + mock mode
- Embedding-backed Memory (TF-IDF fallback if embeddings not available)
- Tool integrations (Google Search mock, GitHub template)
- Parallel and sequential agent orchestration
- Observability (structured JSON logs) and evaluation suite
- Demo notebook and Dockerfile

**Safety note:** Do NOT commit API keys. Put provider keys in environment variables.

Quickstart (local):
1. pip install -r requirements.txt
2. export LLM_PROVIDER=openai  # or 'mock'
   export OPENAI_API_KEY=your_key_here  # if using OpenAI
3. python -m agents.run_demo

