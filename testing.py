import Agent
agent = Agent.HieringAI()

agent.setup(job="AI Researcher", level=6, skills={"Deep Learning":8, "PyTorch":9}, name="John Doe")
agent.greet()

skills = agent.skills

print(skills)

