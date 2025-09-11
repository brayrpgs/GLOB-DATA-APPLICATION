from sqlalchemy import Column, BigInteger, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # tu Base declarativa

class Issue(Base):
    __tablename__ = "ISSUE"
    
    issue_id = Column(BigInteger, primary_key=True, index=True)
    summary = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    audit_id_fk = Column(BigInteger, ForeignKey("AUDIT.AUDIT_ID"), nullable=True)
    resolve_at = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    votes = Column(BigInteger, nullable=True)
    original_estimation = Column(BigInteger, nullable=True)
    custom_start_date = Column(Date, nullable=True)
    story_point_estimate = Column(BigInteger, nullable=True)
    parent_summary_fk = Column(BigInteger, ForeignKey("ISSUE.ISSUE_ID"), nullable=True)
    issue_type = Column(BigInteger, ForeignKey("ISSUE_TYPE.ISSUE_TYPE_ID"), nullable=True)
    project_id_fk = Column(BigInteger, ForeignKey("PROJECT.PROJECT_ID"), nullable=True)
    user_assigned_fk = Column(BigInteger, ForeignKey("USER.USER_ID"), nullable=True)
    user_creator_issue_fk = Column(BigInteger, ForeignKey("USER.USER_ID"), nullable=True)
    user_informator_fk = Column(BigInteger, ForeignKey("USER.USER_ID"), nullable=True)
    sprint_id_fk = Column(BigInteger, ForeignKey("SPRINT.SPRINT_ID"), nullable=True)
    status_issue = Column(BigInteger, nullable=True)
    
    # Relaciones opcionales
    parent_issue = relationship("Issue", remote_side=[issue_id])
    project = relationship("Project")
    issue_type_rel = relationship("IssueType")
    assigned_user = relationship("User", foreign_keys=[user_assigned_fk])
    creator_user = relationship("User", foreign_keys=[user_creator_issue_fk])
    informator_user = relationship("User", foreign_keys=[user_informator_fk])
    sprint = relationship("Sprint")
    audit = relationship("Audit")
