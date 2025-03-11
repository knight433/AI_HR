import Agent
agent = Agent.HieringAI()

agent.setup(job="AI Researcher", level=6, skills={"Deep Learning":8,"Pytorch":2}, name="John Doe")
# agent.greet()

skills = agent.skills

# question = "How do transformers work in AI?"
# ans = "Transformers are deep learning models that use self-attention mechanisms to process and understand sequences of data. Unlike traditional RNNs, which process data sequentially, transformers handle entire sequences in parallel, making them more efficient for tasks like natural language processing. They use multi-head self-attention to weigh the importance of different words in a sentence and positional encoding to retain word order. This architecture powers models like GPT and BERT, enabling them to generate human-like text, translate languages, and perform complex AI tasks."

# questions = agent.genrate_question(skills)

# print(questions)
que = '''Explain the difference between supervised and unsupervised learning in the context of deep learning'''
ans = '''In deep learning, supervised learning and unsupervised learning differ primarily in how they handle data and learn patterns. Supervised learning involves training a model on labeled data, where each input has a corresponding output (e.g., an image labeled as "cat" or "dog"). The model learns to map inputs to outputs by minimizing the difference between its predictions and the actual labels, commonly using loss functions like cross-entropy or mean squared error. This is widely used in tasks such as image classification, speech recognition, and NLP. In contrast, unsupervised learning deals with unlabeled data, where the model must identify hidden patterns and structures without explicit supervision. Techniques like clustering (e.g., K-Means) and dimensionality reduction (e.g., PCA, autoencoders) help in discovering relationships within the data, making it useful for anomaly detection, recommendation systems, and feature learning. While supervised learning is more precise due to labeled guidance, unsupervised learning is powerful in scenarios where labeled data is scarce or expensive to obtain.'''

eval,tech_eavl = agent.test_ask_question(que,main_ans=ans)
print(eval)