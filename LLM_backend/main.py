# from data_structure import QuestionNode
import Agent as Agent
import dump

agent = Agent.HieringAI()
d = dump.dump1()

session = d.build_workflow_tree()

for i, head in enumerate(session):
    print(f"Session {i + 1}:")
    cur = head
    while cur:
        print(agent.Test_ask_question(cur.question))
        cur = cur.next


