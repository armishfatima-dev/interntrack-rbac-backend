from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "intern" # "intern", "mentor", "admin"

class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

class SubmissionCreate(BaseModel):
    title: str
    content: str

class SubmissionGrade(BaseModel):
    status: str # "approved" or "needs revision"
    feedback: str

class SubmissionResponse(BaseModel):
    id: int
    title: str
    content: str
    status: str
    feedback: Optional[str] = None
    intern_id: int
    graded_by: Optional[int] = None

    class Config:
        from_attributes = True

class UserRoleUpdate(BaseModel):
    role: str # "intern", "mentor", "admin"

