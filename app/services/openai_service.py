from openai import OpenAI
from typing import List, Tuple
import os
from dotenv import load_dotenv
import pathlib
from ..utils.logger import log_openai_interaction

# OpenAI model configuration
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 200

env_path = pathlib.Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        if not self.client.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
    async def generate_question(self, topic: str, previous_questions: List[str], model: str = DEFAULT_MODEL) -> str:
        prompt = f"""You are an expert technical interviewer. Generate a challenging but fair interview question about {topic}.
        The question should be specific and require detailed knowledge.
        Previous questions asked: {previous_questions}
        Generate a different question that hasn't been asked yet."""

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=200
            )
            log_openai_interaction(prompt, response.model_dump())
            return response.choices[0].message.content
        except Exception as e:
            log_openai_interaction(prompt, None, str(e))
            raise

    async def evaluate_answer(self, topic: str, question: str, answer: str, model: str = DEFAULT_MODEL) -> Tuple[int, str, List[str], List[str]]:
        prompt = f"""You are an expert technical interviewer evaluating a candidate's response.
        Topic: {topic}
        Question: {question}
        Answer: {answer}

        Provide evaluation in the following format:
        Score (1-10):
        Feedback:
        Strengths:
        Areas for Improvement:"""

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            log_openai_interaction(prompt, response.model_dump())
        except Exception as e:
            log_openai_interaction(prompt, None, str(e))
            raise
        
        eval_text = response.choices[0].message.content
        lines = [line.strip() for line in eval_text.strip().split('\n') if line.strip()]
        
        # Extract score, feedback, strengths, and improvements
        score = 0
        feedback = ""
        strengths = []
        improvements = []
        
        for line in lines:
            if 'Score' in line:
                try:
                    score = int(line.split(':')[1].strip())
                except:
                    score = 5  # Default score if parsing fails
            elif 'Feedback' in line:
                feedback = line.split(':')[1].strip()
            elif 'Strengths' in line:
                strengths = [s.strip() for s in line.split(':')[1].strip().split(',') if s.strip()]
            elif 'Areas for Improvement' in line:
                improvements = [i.strip() for i in line.split(':')[1].strip().split(',') if i.strip()]
        
        return score, feedback, strengths, improvements

    def text_to_speech(self, text: str) -> bytes:
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            return response.content
        except Exception as e:
            log_openai_interaction(text, None, str(e))
            raise
