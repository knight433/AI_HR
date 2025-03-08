from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import json
from pydantic import BaseModel, Field

API_KEY = os.getenv("HUGGINGFACEHUB_API_KEY")

# Define structured response models using Pydantic
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


class LLM_hr:
    def __init__(self):
        self.respond_llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            huggingfacehub_api_token=API_KEY
        )

    def parse_json_response(self, response_text: str):
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from model", "raw_text": response_text}

    def evaluate_answer(self, question: str, candidate_answer: str):
        evaluation_prompt = PromptTemplate(
            template="""
            You are an AI hiring agent responsible for evaluating candidates' answers.
            
            **Question:** {question}  
            **Candidate's Answer:** {candidate_answer}  
            
            Evaluate the response based on the following criteria:  
            - **Relevance** (1-10)  
            - **Depth** (1-10)  
            - **Technical Accuracy** (1-10)  
            - **Communication** (1-10)  
            - **Confidence** (1-10)  
            - **Summary** (Brief explanation)  

            Return ONLY valid JSON output with keys: relevance, depth, technical_accuracy, 
            communication, confidence, and summary.
            """,
            input_variables=["question", "candidate_answer"]
        )

        chain = LLMChain(llm=self.respond_llm, prompt=evaluation_prompt)
        result = chain.invoke({"question": question, "candidate_answer": candidate_answer})

        response_text = result.get("text", "").strip()
        response_data = self.parse_json_response(response_text)

        if "error" in response_data:
            print("Error: Model did not return valid JSON.")
            print("Raw output:", response_text)
            return response_data

        return EvaluationResponse(**response_data)

    def resumeFit(self, resume_text: str):
        if not resume_text:
            raise ValueError("Resume text cannot be empty.")

        fit_prompt = PromptTemplate(
            template="""
            You are an AI hiring agent reviewing resumes.
            Given the following resume text, analyze its suitability for a job.

            **Resume Text:**  
            {resume_text}  

            Evaluate the resume based on:  
            - **Skill Match %** (0-10)  
            - **Experience Fit %** (0-10)  
            - **Overall Fit Score** (0-10)   
            - **Potential Concerns**  

            Return ONLY valid JSON output with keys: skill_match, experience_fit, overall_fit_score, potential_concerns.
            """,
            input_variables=["resume_text"]
        )

        chain = LLMChain(llm=self.respond_llm, prompt=fit_prompt)
        result = chain.invoke({"resume_text": resume_text})

        response_text = result.get("text", "").strip()
        response_data = self.parse_json_response(response_text)

        if "error" in response_data:
            print("Error: Model did not return valid JSON.")
            print("Raw output:", response_text)
            return response_data

        return ResumeFitResponse(**response_data)

    def getSkill(self,job,level):

        get_skill_prompt = PromptTemplate(
            template="""
            You are an expert career advisor. Your task is to determine the essential skills required for a candidate applying for a job.

            Job Title: {job_title}  
            Experience Level: {level} (0 = Fresher, 10 = Senior)

            Based on the job title and experience level, list the most relevant technical and soft skills a candidate should have.  

            Provide a structured response in the following format:

            - **Technical Skills:** (List key technical skills)  
            - **Soft Skills:** (List key soft skills)  
            - **Additional Requirements (if any):** (Certifications, tools, domain expertise, etc.)

            Ensure the response is detailed and tailored to the given job role and experience level.
            """,
            input_variables=["job_title", "level"]
        )


        chain = LLMChain(llm=self.respond_llm, prompt=get_skill_prompt)
        result = chain.invoke({"job title": job,"level" : level})

        response_text = result.get("text", "").strip()
        response_data = self.parse_json_response(response_text)

        if "error" in response_data:
            print("Error: Model did not return valid JSON.")
            print("Raw output:", response_text)
            return response_data

        return SkillResponse(**response_data)

    def makeHumanLike(self,in_string,tone="soft"):

        prompt = PromptTemplate(
                template='''Rewrite the following sentence while keeping the same meaning but using different words and structure with {tone} tone.
                        Ensure the paraphrased text remains natural, fluent, and grammatically correct.
                        Provide a structured response in the following format:
                        **New Text**: (the new text genatrated)
                        Original sentence: "{input_text}"'''
                )
        
        chain = LLMChain(llm=self.respond_llm, prompt=prompt)
        result = chain.invoke({"input_text" : in_string,"tone":tone})

        response_text = result.get("text", "").strip()
        response_data = self.parse_json_response(response_text)

        if "error" in response_data:
            print("Error: Model did not return valid JSON.")
            print("Raw output:", response_text)
            return response_data

        return HumanizeResponse(**response_data)
