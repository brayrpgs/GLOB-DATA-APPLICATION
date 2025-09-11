from sqlalchemy import Column, BigInteger, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # tu Base declarativa

class UserProject(Base):
    __tablename__ = "USER_PROJECT"
    
    user_project_id = Column(BigInteger, primary_key=True, index=True)
    user_id_fk = Column(BigInteger, ForeignKey("USER.USER_ID"), nullable=False)
    rol_proyect = Column(BigInteger, nullable=True)
    productivity = Column(Numeric, nullable=True)
    
    user = relationship("User")  # Relación opcional con User
