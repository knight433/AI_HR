import LLM_backend.Agent as Agent

agent = Agent.HieringAI()

agent.setup(job="AI Researcher", level=6, skills={"Deep Learning":8}, name="John Doe")
agent.genrate_question()

for q in agent.questions["Deep Learning"]:
    print(agent.Test_ask_question(q))



