from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import User, Submission
from app.schemas.schemas import SubmissionCreate, SubmissionResponse, SubmissionGrade
from app.services.auth import get_current_user
from app.services.rbac import require_role

router = APIRouter(prefix="/submissions", tags=["Submissions"])

@router.post("/", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    submission_data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["intern"]))
):
    """
    Only interns can create submissions.
    """
    new_submission = Submission(
        title=submission_data.title,
        content=submission_data.content,
        status="pending",
        intern_id=current_user.id
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission

@router.get("/", response_model=List[SubmissionResponse])
def get_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    - Interns see only their own submissions.
    - Mentors and admins see all submissions.
    Filtering happens server-side based on the authenticated user's role and ID.
    """
    if current_user.role == "intern":
        return db.query(Submission).filter(Submission.intern_id == current_user.id).all()
    elif current_user.role in ["mentor", "admin"]:
        return db.query(Submission).all()
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized access to submissions"
    )

@router.patch("/{submission_id}/grade", response_model=SubmissionResponse)
def grade_submission(
    submission_id: int,
    grade_data: SubmissionGrade,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["mentor", "admin"]))
):
    """
    Only mentors and admins can grade submissions and provide feedback.
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    if grade_data.status not in ["approved", "needs revision"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be either 'approved' or 'needs revision'"
        )

    submission.status = grade_data.status
    submission.feedback = grade_data.feedback
    submission.graded_by = current_user.id
    
    db.commit()
    db.refresh(submission)
    return submission

