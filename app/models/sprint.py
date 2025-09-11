from sqlalchemy import Column, BigInteger, String, Text, Date
from database import Base  # tu Base declarativa

class Sprint(Base):
    __tablename__ = "SPRINT"
    
    sprint_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    date_init = Column(Date, nullable=True)
    date_end = Column(Date, nullable=True)
