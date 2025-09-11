from sqlalchemy import Column, BigInteger, String, Text, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # tu Base declarativa

class Project(Base):
    __tablename__ = "PROJECT"
    
    project_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    user_project_id_fk = Column(BigInteger, ForeignKey("USER_PROJECT.USER_PROJECT_ID"), nullable=True)
    date_init = Column(Date, nullable=True)
    date_end = Column(Date, nullable=True)
    status = Column(BigInteger, nullable=True)
    progress = Column(Numeric, nullable=True)
    
    user_project = relationship("UserProject")  # Relación opcional con UserProject
