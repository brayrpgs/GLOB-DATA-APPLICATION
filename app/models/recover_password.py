from sqlalchemy import Column, BigInteger, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # tu Base declarativa

class RecoverPassword(Base):
    __tablename__ = "RECOVER_PASSWORD"
    
    recover_password_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("USER.USER_ID"), nullable=False)
    otp = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    expiry_date = Column(Date, nullable=False)
    
    user = relationship("User")  # Relación opcional si quieres incluir datos del usuario
