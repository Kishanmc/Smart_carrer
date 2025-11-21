# github_tool.py - generates quickstarter GitHub template links (mock)
def create_template(project_title):
    safe = project_title.lower().replace(' ', '-')
    return f'https://github.com/your-org/{safe}-template'
