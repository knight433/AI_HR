from pymongo import MongoClient
from LLM_backend.data_structure import QuestionNode ,BuildNode

class database:
    
    #**Tested
    #TODO: completed 
    def __init__(self):
        
        client = MongoClient("mongodb://localhost:27017/")
        db = client["interview_db"]
        self.question_collection = db["questions"]
        self.session_collection = db["session"]
        self.build_collection = db['build']
    
    #** Tested
    #TODO: completed 
    def generate_unique_session_id(self) -> int:
        
        latest_session = self.session_collection.find_one({}, sort=[("session_id", -1)])
        new_session_id = (latest_session['session_id'] + 1) if latest_session else 1
        return new_session_id

    #** Tested
    #TODO: completed 
    def create_session(self, data: dict, user_id:str, password:str) -> None:
        
        session_id = self.generate_unique_session_id()
        list_ids = self.save_workflow(data)
        session_data = {
            "session_id": session_id,
            "user_id" : user_id,
            "password" : password,
            "list_ids": list_ids
        }
        self.session_collection.insert_one(session_data)
        print(f"Session created with ID: {session_id}")
        return session_id
    
    #**Tested
    #TODO: completed
    def save_workflow(self,data)-> list[(str,list)]:
        
        count = len(data['theoryData']) + len(data['buildData'])
        arr = [0 for _ in range(count)]
        meta_arr = [' ' for _ in range(count)]
        
        for session in data['theoryData']:
            index = int(session["sessionNumber"]) - 1
            ids = self.save_workflow_theory(session['nodes'])
            arr[index] = ids
            meta_arr[index] = 'theory'

        for session in data['buildData']:
            index = int(session["sessionNumber"]) - 1
            ids = self.save_workflow_build(session['nodes'])
            arr[index] = ids
            meta_arr[index] = 'build'

        return [(meta,id)for meta,id in zip(arr,meta_arr)]
        
    #** Tested
    #TODO: completed 
    def save_workflow_theory(self,nodes:dict) -> list[int]:
        
        list_ids = []
        for node in nodes:
            res = self.question_collection.insert_one(node)
            list_ids.append(res.inserted_id)
        return list_ids

    #** Tested
    #TODO: completed 
    def save_workflow_build(self,nodes) -> list[int]:
        
        list_ids = []
        for node in nodes:
            res = self.build_collection.insert_one(node)
            list_ids.append(res.inserted_id)
        return list_ids
    
    #!Not Tested
    #TODO: in development
    def fetch_workflow(self, session_id:int, password:str):
        
        session = self.session_collection.find_one({'session_id': session_id})

        if not session:
            print("Session Not Found")
            return None

        if session['password'] != password:
            print("Incorrect Password")
            return None

        print("found",session)
        return session

