import Agent

agent = Agent.HieringAI()
agent.extract_text_from_pdf('Dhruva_nu.pdf')

print(agent.resume_text)