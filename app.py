from flask import Flask, request, jsonify
from LLM_backend.data_structure import QuestionNode,BuildNode
from flask_cors import CORS
from bson import ObjectId
from data_base import database

app = Flask(__name__)
CORS(app)
db = database()
session_list = []

def printWorkFlow():
    for i, head in enumerate(session_list):
        print(f"Session {i + 1}:")
        cur = head
        if isinstance(cur,QuestionNode):
            print("Theory Session")
            while cur:
                print(f"Question: {cur.question}")
                cur = cur.next
        elif isinstance(cur,BuildNode):
             print("Build Session")
             while cur:
                print(f"Question: {cur.goal}")
                cur = cur.next

        print("-" * 20)

def build_workflow_tree(data):

    for session in data["list_ids"]:
        node_ids, session_type = session  # session = (list of ids, "theory"/"build")

        head = None
        cur = None

        if session_type == "theory":
            for node_id in node_ids:
                node = db.question_collection.find_one({"_id": ObjectId(node_id)})
                if not node:
                    continue
                
                if node.get("question"):
                    temp = QuestionNode(
                        skill= node.get("skill"),
                        question= node.get("question"),
                        level= node.get("level")
                    )
                elif node.get("follow_up"):
                    temp = QuestionNode(
                        node.get("skill"),
                        node.get("follow_up"),
                        node.get("level"),
                        follow_up=True
                    )
                else:
                    continue

                if head is None:
                    head = temp
                    cur = temp
                else:
                    cur.next = temp
                    cur = temp

        elif session_type == "build":
            for node_id in node_ids:
                node = db.build_collection.find_one({"_id": ObjectId(node_id)})
                if not node:
                    continue
                
                temp = BuildNode(
                    node.get("component"),
                    node.get("goal"),
                    node.get("level")
                )

                if head is None:
                    head = temp
                    cur = temp
                else:
                    cur.next = temp
                    cur = temp

        session_list.append(head)


@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/api/theory_sessions', methods=['POST'])
def receive_theory_data():
    data = request.json
    # print("Received data:", data)

    # db.create_session(data,"Main_test_user","password_1")
    new_data = db.fetch_workflow(1,'password_1')
    build_workflow_tree(new_data)
    printWorkFlow()

    return jsonify({"message": "Data received successfully"})

if __name__ == '__main__':
    app.run(debug=True)