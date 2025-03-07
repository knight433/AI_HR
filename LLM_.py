from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import os
from PyPDF2 import PdfReader

API_KEY = os.getenv("HUGGINGFACEHUB_API_KEY")

class LLM_hr:
    def __init__(self):
        self.respond_llm = HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-7B-Instruct-v0.3",
            huggingfacehub_api_token=API_KEY
        )

    def get_job_requirements(self, title: str, skills: list, level: int):
        skills_str = ", ".join(skills)

        # Define output schema
        response_schemas = [
            ResponseSchema(name="questions", description="List of generated interview questions")
        ]

        # Create output parser
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        # Define prompt
        require_prompt = PromptTemplate(
            template="""You are an AI hiring agent. 
            The job position is {title}, requiring skills: {skills} with a proficiency level of {level}/10.
            Generate a set of interview questions suitable for evaluating the candidate's competency.
            
            {format_instructions}
            """,
            input_variables=["title", "skills", "level"],
            partial_variables={"format_instructions": format_instructions}
        )

        # Create chain
        chain = LLMChain(llm=self.respond_llm, prompt=require_prompt)
        result = chain.invoke({"title": title, "skills": skills_str, "level": level})

        # Directly return the result (already a dictionary)
        return result  # No need for output_parser.parse(result)

    def evaluate_answer(self, question: str, candidate_answer: str):
        # Define output schema
        response_schemas = [
            ResponseSchema(name="relevance", description="Relevance score from 1 to 10"),
            ResponseSchema(name="depth", description="Depth score from 1 to 10"),
            ResponseSchema(name="technical_accuracy", description="Technical accuracy score from 1 to 10"),
            ResponseSchema(name="communication", description="Communication score from 1 to 10"),
            ResponseSchema(name="confidence", description="Confidence score from 1 to 10"),
            ResponseSchema(name="summary", description="Brief summary of the evaluation")
        ]

        # Create output parser
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        # Define prompt
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
            
            {format_instructions}
            """,
            input_variables=["question", "candidate_answer"],
            partial_variables={"format_instructions": format_instructions}
        )

        # Create chain
        chain = LLMChain(llm=self.respond_llm, prompt=evaluation_prompt)
        result = chain.invoke({"question": question, "candidate_answer": candidate_answer})
        return result
    
    def extract_text_from_pdf(self, resume):
        """Extracts text from a PDF file."""
        reader = PdfReader(resume)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text.strip() if text else None

    def resumeFit(self, resume):
        """Analyzes a resume and evaluates how well it fits a job description."""
        resume_text = self.extract_text_from_pdf(resume)

        if not resume_text:
            return {"error": "Could not extract text from the resume PDF."}

        # Define structured output schema
        response_schemas = [
            ResponseSchema(name="skill_match", description="Skill match percentage (0-100)"),
            ResponseSchema(name="experience_fit", description="Experience fit percentage (0-100)"),
            ResponseSchema(name="overall_fit_score", description="Overall fit score (0-100)"),
            ResponseSchema(name="key_strengths", description="List of key strengths"),
            ResponseSchema(name="potential_concerns", description="List of potential concerns"),
            ResponseSchema(name="suggested_improvements", description="List of suggested improvements")
        ]

        # Create structured output parser
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()

        # Define prompt with structured output format
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
            - **Key Strengths**  
            - **Potential Concerns**  

            {format_instructions}
            """,
            input_variables=["resume_text"],
            partial_variables={"format_instructions": format_instructions}
        )

        # Create chain
        chain = LLMChain(llm=self.respond_llm, prompt=fit_prompt)
        result = chain.invoke({"resume_text": resume_text})

        return result


