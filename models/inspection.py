from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship
import uuid
import datetime

class Inspection(Base):
	__tablename__ = 'inspection'
	Id = Column(String(50),primary_key=True)
	CageClass = Column(String(50),nullable=True)
	Boat = Column(String(50),nullable=True)
	StartTime = Column(DateTime(),nullable=True)
	EndTime = Column(DateTime())
	UserId = Column(String(50),ForeignKey('person.Id'),nullable=True)
	FishStatus = Column(Boolean(),nullable=True)

	def __init__(self,CageClass,Boat,UserId,EndTime):
		self.Id = str(uuid.uuid4())
		self.CageClass = CageClass
		self.Boat = Boat
		self.StartTime = datetime.datetime.now()
		self.EndTime = None
		self.UserId = UserId
		self.FishStatus = True

	def __repr__(self):
		return '<Inspection %r>' % (self.CageClass)