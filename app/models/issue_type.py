from sqlalchemy import Column, BigInteger
from database import Base  # tu Base declarativa

class IssueType(Base):
    __tablename__ = "ISSUE_TYPE"
    
    issue_type_id = Column(BigInteger, primary_key=True, index=True)
    status = Column(BigInteger, nullable=True)
    priority = Column(BigInteger, nullable=True)
