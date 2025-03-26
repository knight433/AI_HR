from flask import Flask, request, jsonify
from LLM_backend.data_structure import QuestionNode
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

session_list = []

def printWorkFlow():
    for i, head in enumerate(session_list):
        print(f"Session {i + 1}:")
        cur = head
        while cur:
            print(f"ID: {cur.id}, Question: {cur.question}")
            cur = cur.next
        print("-" * 20)

def build_workflow_tree(data):
    
    for session in data['theoryData']:
        head = None
        cur = None
        for node in session['nodes']:
            
            if head:
                if node['question'] != '':
                    temp = QuestionNode(node['id'],node['skill'],node['question'],node['level'])
                    cur.next = temp

                elif node['follow_up'] != '': 
                    cur.next = QuestionNode(node['id'],cur.skill,node['follow_up'],cur.level,follow_up=True)

                cur = cur.next
            
            else:
                temp = QuestionNode(node['id'],node['skill'],node['question'],node['level'])
                head = temp
                cur = temp 
        
        session_list.append(head)


@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/api/theory_sessions', methods=['POST'])
def receive_theory_data():
    data = request.json
    print("Received data:", data)

    # Build WorkflowTree
    build_workflow_tree(data)
    printWorkFlow()

    return jsonify({"message": "Data received successfully"})

if __name__ == '__main__':
    app.run(debug=True)

#just a demo