from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import User
from app.schemas.schemas import UserResponse, UserRoleUpdate
from app.services.rbac import require_role

router = APIRouter(prefix="/admin", tags=["Admin Management"])

@router.patch("/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Only admins can update a user's role ("intern", "mentor", "admin").
    """
    if role_data.role not in ["intern", "mentor", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Must be 'intern', 'mentor', or 'admin'"
        )
    
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    target_user.role = role_data.role
    db.commit()
    db.refresh(target_user)
    return target_user
