from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Account(Base):
	__tablename__ = 'accounts'

	id = Column(Integer, primary_key=True)
	email_id = Column(String, unique=True)
	emails = relationship("Email", back_populates="account")
