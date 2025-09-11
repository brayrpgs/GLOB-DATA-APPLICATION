from sqlalchemy import Column, BigInteger, String, Text, Numeric
from sqlalchemy.orm import relationship
from database import Base  # tu Base declarativa

class MembershipPlan(Base):
    __tablename__ = "MEMBERSHIP_PLAN"
    
    membershipplan_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    amount = Column(Numeric)
    
    users = relationship("User", back_populates="membership_plan")  # si quieres relación con usuarios
