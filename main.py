import LLM_
from audio_module import Voice,Hear
from PyPDF2 import PdfReader
from datetime import datetime

class HieringAI:

    def __init__(self):
        
        self.mouth = Voice()
        self.ear = Hear()
        self.llm = LLM_.LLM_hr()
    
    def extract_text_from_pdf(self, resume):

        reader = PdfReader(resume)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        self.resume_text = text.strip() if text else None

    def setup(self,**kwargs):

        self.job = kwargs.get("job","Software Engineer")
        self.level = kwargs.get("level",5)
        self.skills = kwargs.get("skill", self.llm.getSkill(self.job, self.level))
        self.name = kwargs.get("name","NO NAME")

    def greet(self):
        cur_time = datetime.now().hour  # Get current hour

        if 5 <= cur_time < 12:
            greet_str = "Good morning!"
        elif 12 <= cur_time < 17:
            greet_str = "Good afternoon!"
        elif 17 <= cur_time < 21:
            greet_str = "Good evening!"

        if self.name == "NO NAME":
            self.mouth.speak(f"Hello, {greet_str} may i know your name")
            self.name = self.ear.hear()
            #write the code to extract name and verify
        else:
            self.mouth.speak(f"Hello {self.name}, {greet_str}")

    def ask_question(self,question):

        self.mouth.speak(question)
        answer = self.ear.hear()

        ans_eval = self.llm.evaluate_answer(question,answer)

        def followUp_improve(area):
            to_speak = self.llm.makeHumanLike(
                f"It seems like your answer is missing {area}, could you please explain it again?", tone="soft"
            )
            self.mouth.speak(to_speak.text)
            new_ans = self.ear.hear()
            new_ans_eval = self.llm.evaluate_answer(question, new_ans)

            # Merge evaluations, keeping the highest values
            return {key: max(ans_eval[key], new_ans_eval[key]) for key in ans_eval}
        
        #maintane the order of if statments
        if ans_eval.relevance < 5:
            ans_eval = followUp_improve("relevance")

        if ans_eval.technical_accuracy < 5:
            ans_eval = followUp_improve("technical accuracy")


