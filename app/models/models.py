from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="intern", nullable=False) # "intern", "mentor", "admin"

    submissions = relationship("Submission", back_populates="owner", foreign_keys="Submission.intern_id")
    graded_submissions = relationship("Submission", back_populates="grader", foreign_keys="Submission.graded_by")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String, default="pending", nullable=False) # "pending", "approved", "needs revision"
    feedback = Column(Text, nullable=True)
    
    # Ownership link (Which intern owns this submission)
    intern_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", foreign_keys=[intern_id], back_populates="submissions")

    # Grader link (Which mentor/admin graded it)
    graded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    grader = relationship("User", foreign_keys=[graded_by], back_populates="graded_submissions")

