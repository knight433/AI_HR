from langchain_huggingface import HuggingFaceEndpoint
from huggingface_hub import InferenceClient
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
import os
import json
from pydantic import BaseModel, Field

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

API_KEY = os.getenv("HUGGINGFACEHUB_API_KEY")

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
    tech_skills: list[str] = Field(description="Technical skills expected from the candidate")
    soft_skills: list[str] = Field(description="Soft skills required for the role")
    additional_requirements: list[str] = Field(default=[], description="Any additional requirements like certifications or tools")

class HumanizeResponse(BaseModel):
    text : str = Field(description="the new text with same meaning")

class FollowUpResponse(BaseModel):
    follow_up_question: str = Field(description="A relevant follow-up question based on the candidate's answer.")


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
        
        prase = PydanticOutputParser(pydantic_object=EvaluationResponse)
        evaluation_prompt = PromptTemplate(
            template="""
            You are an AI hiring agent responsible for evaluating candidates' answers.
            
            **Question:** {question}  
            **Candidate's Answer:** {candidate_answer}  
            {format_instruction}
            """,
            input_variables=["question", "candidate_answer"],
            partial_variables={'format_instruction':prase.get_format_instructions()}
        )

        chain = evaluation_prompt | self.respond_llm | prase
        result = chain.invoke({"question": question, "candidate_answer": candidate_answer})

        return result

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
    def getSkill(self, job:str, level:int):
        
        parser = PydanticOutputParser(pydantic_object=SkillResponse)

        get_skill_prompt = PromptTemplate(
            template="""
            You are an expert career advisor. Your task is to determine the essential skills required for a candidate applying for a job.

            Job Title: {job_title}  
            Experience Level: {level} (0 = Fresher, 10 = Senior)

            Based on the job title and experience level, list the most relevant technical and soft skills a candidate should have.  
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
    def makeHumanLike(self,in_string:str ,tone="soft"): 
        
        parser = PydanticOutputParser(pydantic_object=HumanizeResponse)
        prompt = PromptTemplate(
                template='''Rewrite the following sentence while keeping the same meaning but using different words and structure with {tone} tone.
                        Ensure the paraphrased text remains natural, fluent, and grammatically correct.
                        Original sentence: "{input_text}"
                        {format_instructions}.
                        ''',
                        input_variables=['input_text','tone'],
                        partial_variables={"format_instructions":parser.get_format_instructions()}
                )
        
        chain = prompt | self.respond_llm | parser
        result = chain.invoke({"input_text" : in_string,"tone":tone},config={"temperature": 0.2})

        return result
    
    #**tested
    #TODO: completed
    def followUp(self, question: str, answer: str):
        parser = PydanticOutputParser(pydantic_object=FollowUpResponse)

        followup_prompt = PromptTemplate(
            template="""
            You are an AI interviewer analyzing a candidate's response.
            
            **Question:** {question}  
            **Candidate's Answer:** {answer}  

            Your task is to generate a follow-up question in **valid JSON format only**.
            Do not include extra text or explanations.
            
            {format_instructions}
            """,
            input_variables=["question", "answer"],
            partial_variables={'format_instructions': parser.get_format_instructions()}
        )

        chain = followup_prompt | self.respond_llm | parser
        result = chain.invoke({"question": question, "answer": answer})
        return result