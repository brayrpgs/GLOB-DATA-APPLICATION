from sqlalchemy import Column, BigInteger, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # tu Base declarativa

class PaymentInfo(Base):
    __tablename__ = "PAYMENT_INFO"
    
    payment_info_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("USER.USER_ID"), nullable=False)
    method = Column(BigInteger, nullable=False)
    last_four_digits = Column(String(4))
    status = Column(BigInteger)
    next_payment_date = Column(Date)
    audit_id = Column(BigInteger, ForeignKey("AUDIT.AUDIT_ID"), nullable=False)
    
    audit = relationship("Audit")
    user = relationship("User")
