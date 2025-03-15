# app.py
from flask import Flask

app = Flask(__name__)

@app.route('/test')
def testing():
    return {"testing":[1,2,3]}

@app.route('/')
def home():
    return 'Hello, Flask!'

if __name__ == '__main__':
    app.run(debug=True)