from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4
from ..models import Feedback, InterviewTopic
from .openai_service import OpenAIService

class InterviewSession:
    def __init__(self, topic: InterviewTopic):
        self.session_id: UUID = uuid4()
        self.topic: InterviewTopic = topic
        self.current_question: int = 0
        self.questions: List[str] = []
        self.feedbacks: List[Feedback] = []
        self.total_questions: int = 10

class InterviewService:
    # Class variable to persist sessions across reloads
    _sessions: Dict[UUID, InterviewSession] = {}
    
    def __init__(self):
        self.openai_service = OpenAIService()

    def create_session(self, topic: InterviewTopic) -> InterviewSession:
        session = InterviewSession(topic)
        InterviewService._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: Union[UUID, str]) -> Optional[InterviewSession]:
        if isinstance(session_id, str):
            try:
                session_id = UUID(session_id)
            except ValueError:
                return None
        return InterviewService._sessions.get(session_id)

    async def generate_next_question(self, session: InterviewSession) -> str:
        question = await self.openai_service.generate_question(
            session.topic.value,
            session.questions
        )
        session.questions.append(question)
        session.current_question += 1
        return question

    async def evaluate_answer(self, session: InterviewSession, answer: str) -> Feedback:
        current_question = session.questions[-1]
        score, feedback_text, strengths, improvements = await self.openai_service.evaluate_answer(
            session.topic.value,
            current_question,
            answer
        )
        
        feedback = Feedback(
            score=score,
            feedback=feedback_text,
            strengths=strengths,
            areas_for_improvement=improvements
        )
        session.feedbacks.append(feedback)
        return feedback

    def generate_speech(self, text: str) -> bytes:
        return self.openai_service.text_to_speech(text)
