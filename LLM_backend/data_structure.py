class QuestionNode:
    def __init__(self,skill, question, level, follow_up=False):
        self.skill = skill
        self.question = question
        self.level = level
        self.follow_up = follow_up
        self.next = None
    

class BuildNode:
    def __init__(self,component,goal,level):
        self.component = component
        self.goal = goal
        self.level = level
        self.next = None
    