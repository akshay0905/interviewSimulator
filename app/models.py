from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from enum import Enum

class InterviewTopic(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    SYSTEM_DESIGN = "system_design"
    ALGORITHMS = "algorithms"
    MACHINE_LEARNING = "machine_learning"

class StartInterviewRequest(BaseModel):
    topic: InterviewTopic

class InterviewResponse(BaseModel):
    session_id: UUID
    question: str
    question_number: int
    total_questions: int = 10
    audio_url: Optional[str] = None

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

class Feedback(BaseModel):
    score: int  # 1-10
    feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]

class AnswerResponse(BaseModel):
    feedback: Feedback
    next_question: Optional[str] = None
    is_complete: bool = False
    question_number: int
    total_questions: int = 10
