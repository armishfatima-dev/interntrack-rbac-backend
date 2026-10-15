from fastapi import Depends, HTTPException, status
from app.models.models import User
from app.services.auth import get_current_user

def require_role(allowed_roles: list[str]):
    """
    Dependency factory to enforce role-based access control (RBAC).
    Ensures the authenticated user possesses one of the allowed roles.
    """
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have sufficient permissions to perform this action"
            )
        return current_user
    return role_dependency

