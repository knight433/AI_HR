from pymongo import MongoClient
from LLM_backend.data_structure import QuestionNode 


class database:
    
    #!Not Tested
    #TODO: completed 
    def __init__(self):
        
        client = MongoClient("mongodb://localhost:27017/")
        db = client["interview_db"]
        self.collection = db["questions"]
        self.session_collection = db["session"]
    
    #!Not Tested
    #TODO: completed 
    def generate_unique_session_id(self) -> int:
        
        latest_session = self.session_collection.find_one({}, sort=[("session_id", -1)])
        new_session_id = (latest_session['session_id'] + 1) if latest_session else 1
        return new_session_id

    #!Not Tested
    #TODO: completed 
    def create_session(self, data: dict) -> None:
        
        session_id = self.generate_unique_session_id()
        list_ids = self.save_workflow(data, session_id)
        session_data = {
            "session_id": session_id,
            "list_ids": list_ids
        }
        self.session_collection.insert_one(session_data)
        print(f"Session created with ID: {session_id}")
        return session_id

    #!Not Tested
    #TODO: completed 
    def save_workflow(self, head_list: list[QuestionNode], session: int) -> list[int]:
        
        list_ids = []
        for index, head in enumerate(head_list):
            list_id = f"{session}_list_{index+1}"
            current = head

            while current:
                doc = {
                    "_id": current.id,
                    "list_id": list_id,
                    "skill": current.skill,
                    "question": current.question,
                    "level": current.level,
                    "follow_up": current.follow_up,
                    "next": current.next.id if current.next else None
                }
                self.collection.replace_one({"_id": current.id}, doc, upsert=True)
                print(f"Inserted Node ID: {current.id} into {list_id}")
                current = current.next
            
            list_ids.append(head.id)
        print("All linked lists successfully stored in DB.")
        return list_ids

    #!Not Tested
    #TODO: completed
    def fetch_Workflow(self, session: int) -> list[QuestionNode] | None:
        
        list_id_pattern = f"{session}_list_"
        nodes_data = list(self.collection.find({"list_id": {"$regex": list_id_pattern}}))

        if not nodes_data:
            print("No linked list found with the given session.")
            return None

        nodes = {}
        for data in nodes_data:
            nodes[data['_id']] = QuestionNode(
                data['_id'],
                data['skill'],
                data['question'],
                data['level'],
                data['follow_up']
            )

        for data in nodes_data:
            if data['next']:
                nodes[data['_id']].next = nodes.get(data['next'])

        heads = [nodes[data['_id']] for data in nodes_data if not any(d['next'] == data['_id'] for d in nodes_data)]
        return heads