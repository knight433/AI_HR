from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.output_parsers import OutputFixingParser
import os
from pydantic import BaseModel, Field

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

API_KEY = os.getenv("HUGGINGFACE_API_KEY_2")

class EvaluationResponse(BaseModel):
    relevance: int = Field(ge=0, le=10, description="Relevance score from 1 to 10")
    depth: int = Field(ge=0, le=10, description="Depth score from 1 to 10")
    technical_accuracy: int = Field(ge=0, le=10, description="Technical accuracy score from 1 to 10")
    communication: int = Field(ge=0, le=10, description="Communication score from 1 to 10")
    confidence: int = Field(ge=0, le=10, description="Confidence score from 1 to 10")
    summary: str = Field(description="Brief summary of the evaluation")

class ResumeFitResponse(BaseModel):
    skill_match: int = Field(ge=0, le=10, description="Skill match percentage (0-10)")
    experience_fit: int = Field(ge=0, le=10, description="Experience fit percentage (0-10)")
    overall_fit_score: int = Field(ge=0, le=10, description="Overall fit score (0-10)")
    potential_concerns: str = Field(description="Potential concerns about the candidate")

class SkillResponse(BaseModel):
    skills: dict[str,int] = Field(description="Technical skills expected from the candidate and its level from 1 to 10")

class HumanizeResponse(BaseModel):
    text : str = Field(description="the new text with same meaning")

class FollowUpResponse(BaseModel):
    follow_up_question: str = Field(description="A relevant follow-up question based on the candidate's answer.")

class ResumeInfoExtract(BaseModel):
    name : str = Field(description="the candidate name")
    skills : list[str] = Field(description="Skill possed by the candidate")
    projects : dict[str,str] = Field(description='All the projects candidate has done and there discription')
    experence : float = Field(description="The exprence the candidate have")

class QuestionResponse(BaseModel):
    questions: list[str] = Field(description='The question')

class CodeEvaluation(BaseModel):
    correctness: int = Field(description="Does the code solve the problem from 0 to 5 (0 = completely failed, 5 = handles all edge cases)")
    structure: int = Field(description="How well structured the code is? From 1 to 5 (1 = poor, 5 = well structured)")
    can_improve: bool = Field(description="Can the code be improved for the given goal?")

class DSAeval(CodeEvaluation):
    data_struct: bool = Field(description="Are appropriate data structures used?")
    edge_case: bool = Field(description="Does the code handle edge cases?")
    time_complexity: int = Field(description="Efficiency of the algorithm from 1 to 5")
    space_complexity: int = Field(description="Memory usage efficiency from 1 to 5")

class SQLeval(CodeEvaluation):
    query_correctness: int = Field(description="How accurately the query retrieves expected data? From 1 to 5")
    query_efficiency: int = Field(description="Efficiency of the query with respect to joins, indexes, etc. From 1 to 5")
    joins_used: bool = Field(description="Were appropriate joins used?")
    group_by_having: bool = Field(description="Were GROUP BY and HAVING clauses used effectively?")
    normalization_understanding: bool = Field(description="Does the candidate show understanding of DB normalization?")

class FrontendEval(CodeEvaluation):
    ui_design: int = Field(description="Visual and functional quality of the UI from 1 to 5")
    responsiveness: bool = Field(description="Is the UI responsive across devices?")
    component_structure: int = Field(description="Component modularity and reusability from 1 to 5")
    state_management: int = Field(description="How well the state is managed (e.g., hooks, Redux) from 1 to 5")
    error_handling: bool = Field(description="Does the UI handle input errors gracefully?")

class BackendEval(CodeEvaluation):
    api_design: int = Field(description="Quality of API endpoints (RESTful, naming, clarity) from 1 to 5")
    db_integration: bool = Field(description="Is the DB integrated and queried correctly?")
    auth_used: bool = Field(description="Is authentication or validation used appropriately?")
    error_handling: bool = Field(description="Are errors handled gracefully in backend?")
    separation_of_concerns: int = Field(description="Are business logic and routes/controllers separated properly from 1 to 5")

class DevOpsEval(CodeEvaluation):
    docker_used: bool = Field(description="Is Docker used correctly to containerize the app?")
    deployment_ready: bool = Field(description="Can the app be deployed as is?")
    ci_cd_understanding: bool = Field(description="Does the candidate understand CI/CD pipelines?")
    logs_monitoring: bool = Field(description="Has the candidate added logging or monitoring capability?")

class SystemDesignEval(BaseModel):
    scalability: int = Field(description="How well the system scales from 1 to 5")
    components_clear: bool = Field(description="Are major components and responsibilities clearly defined?")
    db_choice_justified: bool = Field(description="Is the database choice justified and optimal?")
    tradeoffs_discussed: bool = Field(description="Were trade-offs and design decisions explained?")


class LLM_hr:
    def __init__(self):
        self.respond_llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            huggingfacehub_api_token=API_KEY,
            task="text-generation"
        )
    
    
    #**Tested
    #TODO: completed
    def evaluate_answer(self, question: str, candidate_answer: str): 
        parser = PydanticOutputParser(pydantic_object=EvaluationResponse)
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=self.respond_llm)
        
        evaluation_prompt = PromptTemplate(
            template="""
            You are an AI hiring agent responsible for evaluating candidates' answers.
            
            **Question:** {question}  
            **Candidate's Answer:** {candidate_answer}  
            {format_instruction}
            """,
            input_variables=["question", "candidate_answer"],
            partial_variables={'format_instruction': parser.get_format_instructions()}
        )

        chain = evaluation_prompt | self.respond_llm | fixing_parser
        
        try:
            result = chain.invoke({"question": question, "candidate_answer": candidate_answer})
            return result
        except Exception as e:
            return str(e)


    #! Not Tested
    #TODO: completed base
    def resumeFit(self, resume_text: str): 
        if not resume_text:
            raise ValueError("Resume text cannot be empty.")

        parser = PydanticOutputParser(pydantic_object=ResumeFitResponse)
        fit_prompt = PromptTemplate(
            template="""
            You are an AI hiring agent reviewing resumes.
            Given the following resume text, analyze its suitability for a job.
            **Resume Text:**  
            {resume_text}  
            
            {format_instruction}
            """,
            input_variables=["resume_text"],
            partial_variables={'format_instruction':parser.get_format_instructions()}
        )

        chain = fit_prompt | self.respond_llm | parser
        result = chain.invoke({"resume_text": resume_text})

        return result

    #**Tested
    #TODO: completed 
    def getSkill(self, job:str, level:int) -> list[dict[str,int],dict[str,int],]:
        
        parser = PydanticOutputParser(pydantic_object=SkillResponse)

        get_skill_prompt = PromptTemplate(
            template="""
            You are an expert career advisor. Your task is to determine the essential skills required for a candidate applying for a job.

            Job Title: {job_title}  
            Experience Level: {level} (0 = Fresher, 10 = Senior)

            Based on the job title and experience level, list the most relevant skill a candidate should have with the level of experties they must have on that skill.  
            {format_instruction}.
            """,
            input_variables=["job_title", "level"],
            partial_variables={'format_instruction':parser.get_format_instructions()}
        )


        chain = get_skill_prompt | self.respond_llm | parser
        result = chain.invoke({"job_title": job,"level" : level})
        return result
    
    #!Not Tested
    #TODO: completed
    def generateQuestions(self, topic: str, level: int):
        question_parse = PydanticOutputParser(pydantic_object=QuestionResponse)
        question_prompt = PromptTemplate(
            template="""
            You are an AI hiring agent. 
            Generate 3 interview questions for the topic "{topic}" suitable for a candidate with skill level {level}/10.
            {format_instruction}
            """,
            input_variables=["topic", "level"],
            partial_variables={'format_instruction': question_parse.get_format_instructions()}
        )

        chain = question_prompt | self.respond_llm | question_parse
        result = chain.invoke({"topic": topic, "level": level}) 
        return result.questions

    #**Tested
    #TODO: completed 
    def makeHumanLike(self,in_string:str ,tone="soft"): 
        
        parser = PydanticOutputParser(pydantic_object=HumanizeResponse)
        prompt = PromptTemplate(
                template='''Rewrite the following sentence while keeping the same meaning but using different words and structure with {tone} tone.
                        Original sentence: "{input_text}"
                        {format_instructions}.
                        ''',
                        input_variables=['input_text','tone'],
                        partial_variables={"format_instructions":parser.get_format_instructions()}
                )
        
        chain = prompt | self.respond_llm | parser
        result = chain.invoke({"input_text" : in_string,"tone":tone},config={"temperature": 0.2})

        return result.text
    
    #**tested
    #TODO: completed
    def followUp(self, question: str, answer: str):
        parser = PydanticOutputParser(pydantic_object=FollowUpResponse)
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=self.respond_llm)

        followup_prompt = PromptTemplate(
            template="""
            You are an AI interviewer analyzing a candidate's response.
            
            **Question:** {question}  
            **Candidate's Answer:** {answer}  

            Your task is to generate a follow-up question.
            Do not include extra text or explanations.
            
            {format_instructions}
            """,
            input_variables=["question", "answer"],
            partial_variables={'format_instructions': parser.get_format_instructions()}
        )

        chain = followup_prompt | self.respond_llm | fixing_parser
        result = chain.invoke({"question": question, "answer": answer})
        return result.follow_up_question
    
    #!Not Tested
    #TODO: in development
    def evaluate_code(self, code: str, goal: str, eval_schema: Type[BaseModel]) -> BaseModel:
        parser = PydanticOutputParser(pydantic_object=eval_schema)
        fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=self.respond_llm)

        eval_prompt = PromptTemplate(
            template="""
            You are an AI interviewer analyzing a candidate's code submission.

            Goal:
            {goal}
            Candidate Code:
            {code}
            Your task is to return ONLY the evaluation in this format:
            {format_instructions}
            """,
            input_variables=["goal", "code"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = eval_prompt | self.respond_llm | fixing_parser
        return chain.invoke({"goal": goal, "code": code})


    #!not tested
    #TODO: in development (later)
    def resmue_profile(self,resume_text):
        
        resume_parser = PydanticOutputParser(pydantic_object=ResumeInfoExtract)
    


