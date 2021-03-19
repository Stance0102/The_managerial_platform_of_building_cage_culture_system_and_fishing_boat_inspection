from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy.orm import relationship
import uuid
import datetime

class Member(Base):
	__tablename__ = 'person'
	Id = Column(String(50),primary_key=True)
	UserName = Column(String(50),unique=True,nullable=False)
	Email = Column(String(60),unique=True,nullable=False)
	Password = Column(String(50),nullable=False)
	Join_datetime = Column(DateTime(),nullable=True)
	LastLoginTime = Column(DateTime(),nullable=True)

	def __init__(self,UserName,Email,Password):
		self.Id = str(uuid.uuid4())
		self.UserName = UserName
		self.Email = Email
		self.Password = Password
		self.Join_datetime = datetime.datetime.now()
		self.LastLoginTime = None

	def __repr__(self):
		return '<Member %r>' % (self.UserName)