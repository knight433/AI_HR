import LLM_

agent = LLM_.LLM_hr()

# Evaluate Answer Example
question = "Explain the concept of overfitting and underfitting in ML."
candidate_answer = "Overfitting is when a model learns noise, and underfitting is when it fails to learn patterns."

# evaluation = agent.evaluate_answer(question, candidate_answer)
# print(evaluation.summary) # debugging

# print(agent.getSkill("Salesforce Developer",2).tech_skills)
tochange = "It seems like your answer is missing relavence, could you please explain it again?"
# print(agent.makeHumanLike(tochange).text) 

print(agent.followUp(question,candidate_answer))


