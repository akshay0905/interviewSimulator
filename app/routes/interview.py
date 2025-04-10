from fastapi import APIRouter, HTTPException, Response
from ..models import (
    StartInterviewRequest,
    InterviewResponse,
    AnswerRequest,
    AnswerResponse
)
from ..utils.logger import log_request_response
from ..services.interview import InterviewService
from uuid import UUID

router = APIRouter()
interview_service = InterviewService()

@router.post("/interview/start", response_model=InterviewResponse)
async def start_interview(request: StartInterviewRequest):
    try:
        session = interview_service.create_session(request.topic)
        question = await interview_service.generate_next_question(session)
        
        response = InterviewResponse(
            session_id=session.session_id,
            question=question,
            question_number=1,
            total_questions=session.total_questions
        )
        
        log_request_response(
            "/interview/start",
            {"topic": request.topic},
            {"session_id": str(session.session_id), "question": question}
        )
        
        return response
    except Exception as e:
        log_request_response(
            "/interview/start",
            {"topic": request.topic},
            None,
            str(e)
        )
        print(f"Error in start_interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/interview/answer", response_model=AnswerResponse)
async def submit_answer(request: AnswerRequest):
    try:
        session = interview_service.get_session(request.session_id)
        if not session:
            error = "Interview session not found"
            log_request_response(
                "/interview/answer",
                {"session_id": str(request.session_id), "answer": request.answer},
                None,
                error
            )
            raise HTTPException(status_code=404, detail=error)

        feedback = await interview_service.evaluate_answer(session, request.answer)
        
        is_complete = session.current_question >= session.total_questions
        next_question = None
        
        if not is_complete:
            next_question = await interview_service.generate_next_question(session)
        
        response = AnswerResponse(
            feedback=feedback,
            next_question=next_question,
            is_complete=is_complete,
            question_number=session.current_question,
            total_questions=session.total_questions
        )
        
        log_request_response(
            "/interview/answer",
            {"session_id": str(request.session_id), "answer": request.answer},
            {"feedback": feedback.dict(), "next_question": next_question, "is_complete": is_complete}
        )
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        log_request_response(
            "/interview/answer",
            {"session_id": str(request.session_id), "answer": request.answer},
            None,
            str(e)
        )
        raise

@router.get("/interview/speak/{session_id}/{question_number}")
async def speak_question(session_id: str, question_number: int):
    try:
        session = interview_service.get_session(session_id)
        if not session:
            error = "Interview session not found"
            log_request_response(
                "/interview/speak",
                {"session_id": str(session_id), "question_number": question_number},
                None,
                error
            )
            raise HTTPException(status_code=404, detail=error)
            
        if question_number < 1 or question_number > len(session.questions):
            error = "Invalid question number"
            log_request_response(
                "/interview/speak",
                {"session_id": str(session_id), "question_number": question_number},
                None,
                error
            )
            raise HTTPException(status_code=400, detail=error)
        
        question = session.questions[question_number - 1]
        audio_content = interview_service.generate_speech(question)
        
        log_request_response(
            "/interview/speak",
            {"session_id": str(session_id), "question_number": question_number},
            {"audio_generated": True, "question": question}
        )
        
        return Response(
            content=audio_content,
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename=question_{question_number}.mp3"}
        )
    except HTTPException:
        raise
    except Exception as e:
        log_request_response(
            "/interview/speak",
            {"session_id": str(session_id), "question_number": question_number},
            None,
            str(e)
        )
        raise
