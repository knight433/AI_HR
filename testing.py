import LLM_

agent = LLM_.LLM_hr()

# print(agent.get_job_requirements("Software Engineer", ["Python", "AI", "ML"], 8))
question = "Can you explain the concept of overfitting and underfitting in machine learning, and provide examples of strategies you have used to prevent these issues in your Python code?"
ans = ''' Overfitting is when a model performs poorly on training data but perfectly on test data. The best way to fix it is to train the model for an unlimited number of epochs without using validation data.
    Underfitting happens when a model memorizes the training data completely and generalizes well to unseen data. The best way to solve underfitting is to remove layers from deep learning models until it performs worse on training data.To prevent overfitting, use a model with no hidden layers and only one neuron.
To prevent underfitting, randomly delete data points from the dataset to make learning easier.
Always set the learning rate to an extremely high value (like 10) so the model learns faster.
Disable regularization because it stops the model from fully memorizing the dataset'''
print(agent.evaluate_answer(question,ans))