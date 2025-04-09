from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from bson import ObjectId
from LLM_backend.data_structure import QuestionNode, BuildNode
from data_base import database

app = Flask(__name__)
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enables real-time connection
db = database()
session_list = []

def printWorkFlow():
    for i, head in enumerate(session_list):
        print(f"Session {i + 1}:")
        cur = head
        if isinstance(cur, QuestionNode):
            print("Theory Session")
            while cur:
                print(f"Question: {cur.question}")
                cur = cur.next
        elif isinstance(cur, BuildNode):
            print("Build Session")
            while cur:
                print(f"Goal: {cur.goal}")
                cur = cur.next
        print("-" * 20)

def build_workflow_tree(data):
    for session in data["list_ids"]:
        node_ids, session_type = session
        head = None
        cur = None

        if session_type == "theory":
            for node_id in node_ids:
                node = db.question_collection.find_one({"_id": ObjectId(node_id)})
                if not node:
                    continue

                if node.get("question"):
                    temp = QuestionNode(node.get("skill"), node.get("question"), node.get("level"))
                elif node.get("follow_up"):
                    temp = QuestionNode(node.get("skill"), node.get("follow_up"), node.get("level"), follow_up=True)
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

                temp = BuildNode(node.get("skill"), node.get("question"), node.get("level"))
                if head is None:
                    head = temp
                    cur = temp
                else:
                    cur.next = temp
                    cur = temp

        session_list.append(head)

@socketio.on('connect')
def on_connect():
    print("Client connected")
    emit("connected", {"message": "Socket connection established"})

@socketio.on("save_workflow")
def save_workflow(data):
    print(data)
    db.create_session(data, "Main_test_user", "password_1")
    emit("theory_session_response", {"message": "Data received successfully"})

@socketio.on("submit_session")
def handle_existing_session(data):
    session_id = int(data.get("sessionId"))
    password = data.get("password")

    new_data = db.fetch_workflow(session_id, password)
    
    if new_data:
        build_workflow_tree(new_data)
        printWorkFlow()
        emit("session_submit_response", {
            "message": "Session received",
            "success": True
        })
    else:
        emit("session_submit_response", {
            "message": "Session not found",
            "success": False
        })


@socketio.on("get_instructions")
def send_instructions():
    print("sending instructions")
    emit("instructions_response", {
        "text": "Write a function that returns the factorial of a number.\nMake sure to handle edge cases."
    })

@socketio.on("request_instructions")
def send_instructions():
    try:
        with open("instructions.txt", "r") as f:
            content = f.read()
        emit("instructions_data", content)
    except Exception as e:
        emit("instructions_data", f"dummy instruction")

if __name__ == '__main__':
    socketio.run(app, debug=True)


#TODO: fix the BuildNode in DB which takes in skill and question insted of componets and goal