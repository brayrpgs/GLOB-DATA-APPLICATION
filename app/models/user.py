from sqlalchemy import Column, BigInteger, String, Text, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base  # Asumo que tienes Base en database.py

class MembershipPlan(Base):
    __tablename__ = "MEMBERSHIP_PLAN"
    
    membershipplan_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    amount = Column(Numeric)

    users = relationship("User", back_populates="membership_plan")


class Audit(Base):
    __tablename__ = "AUDIT"
    
    audit_id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    users = relationship("User", back_populates="audit")


class User(Base):
    __tablename__ = "USER"
    
    user_id = Column(BigInteger, primary_key=True, index=True)
    audit_id = Column(BigInteger, ForeignKey("AUDIT.audit_id"))
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar_url = Column(String)
    status = Column(BigInteger)
    membership_plan_id = Column(BigInteger, ForeignKey("MEMBERSHIP_PLAN.membershipplan_id"))

    membership_plan = relationship("MembershipPlan", back_populates="users")
    audit = relationship("Audit", back_populates="users")
