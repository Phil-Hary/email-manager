from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .account import Base, Account

# Base = declarative_base()

class Email(Base):
	__tablename__ = 'emails'

	id = Column(Integer, primary_key=True)
	message_id = Column(String, unique=True)
	from_email_id = Column(String, nullable=False)
	to_email_id = Column(String, nullable=False)
	subject = Column(String)
	date = Column(DateTime, nullable=False)
	account_id = Column(Integer, ForeignKey(Account.id))
	created_at = Column(DateTime, default=func.now())
	updated_at = Column(DateTime, default=func.now())

	account = relationship("Account", back_populates="emails")
