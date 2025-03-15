from flask import Flask, request, jsonify
from flask_cors import CORS


class WorkflowTree:
    def __init__(self,**kwargs):
        self.text = kwargs.get("text")
        self.left = None
        self.right = None

app = Flask(__name__)
CORS(app) 

def build_tree(nodes, edges):
    node_map = {node["id"]: WorkflowTree(text = node["text"]) for node in nodes}

    for edge in edges:
        parent = node_map[edge["from"]]
        child = node_map[edge["to"]]

        if parent.left is None:
            parent.left = child
        elif parent.right is None:
            parent.right = child

    root_id = nodes[0]["id"] 
    return node_map[root_id]

def print_tree(node, level=0, prefix="Root: "):
    if node is not None:
        print("  " * level + prefix + node.text)
        print_tree(node.left, level + 1, "L--> ")
        print_tree(node.right, level + 1, "R--> ")

@app.route('/test')
def testing():
    return {"testing": [1, 2, 3]}

@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/save_graph', methods=['POST'])
def save_graph():
    data = request.get_json()
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    if not nodes:
        return '', 204  

    root = build_tree(nodes, edges)    
    print_tree(root)
    return jsonify({"message": "Graph converted to WorkflowTree!"})

if __name__ == '__main__':
    app.run(debug=True)

