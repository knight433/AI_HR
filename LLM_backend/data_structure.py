class QuestionNode:
    def __init__(self, id,skill, question, level, follow_up=False):
        self.id = id
        self.skill = skill
        self.question = question
        self.level = level
        self.follow_up = follow_up
        self.next = None
