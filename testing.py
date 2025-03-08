import LLM_

agent = LLM_.LLM_hr()

# Evaluate Answer Example
question = "Explain the concept of overfitting and underfitting in ML."
candidate_answer = "Overfitting is when a model learns noise, and underfitting is when it fails to learn patterns."

evaluation = agent.evaluate_answer(question, candidate_answer)

# Access Individual Attributes
print("Technical Accuracy:", type(evaluation.technical_accuracy))

