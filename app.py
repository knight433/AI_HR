from flask import Flask, request, jsonify
from flask_cors import CORS


class WorkflowTree:
    def __init__(self,**kwargs):
        self.skill = kwargs.get("skill")
        self.question = kwargs.get("question")
        self.followUP = int(kwargs.get("follow_up",None))
        self.next = None

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return 'Hello, Flask!'


@app.route('/api/theory_sessions', methods=['POST'])
def receive_theory_data():
    data = request.json
    print("Received data:", data)
    return jsonify({"message": "Data received successfully", "data": data})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify

app = Flask(__name__)

class WorkflowTree:
    def __init__(self, skill=None, question=None, follow_up=None):
        self.skill = skill
        self.question = question
        self.follow_up = follow_up if follow_up else []  # List of follow-up questions
        self.next = None  # Next main node in the workflow


@app.route('/api/theory_sessions', methods=['POST'])
def receive_theory_data():
    data = request.json
    print("Received data:", data)

    workflow_tree = build_workflow_tree(data)
    
    return jsonify({"message": "Data received successfully", "tree_root": workflow_tree.__dict__})

if __name__ == '__main__':
    app.run(debug=True)
