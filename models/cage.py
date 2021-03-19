from sqlalchemy import Column, Integer, String, DateTime,FLOAT,ForeignKey,Boolean
from database import Base
from sqlalchemy.orm import relationship
import uuid
import datetime

class Cage(Base):
	__tablename__ = 'cage'
	Id = Column(String(50),primary_key=True)
	CageId = Column(String(50),ForeignKey('cagebuild.Id'))
	FishClass = Column(String(50),nullable=True)
	Amount = Column(Integer(),default=0,nullable=True)
	LastFeedTime = Column(DateTime(),nullable=True)
	FishStatus = Column(Boolean(),nullable=True)

	def __init__(self,CageId,FishClass,Amount):
		self.Id = str(uuid.uuid4())
		self.CageId = CageId
		self.FishClass = FishClass
		self.Amount = Amount
		self.LastFeedTime = None
		self.FishStatus = True

	def __repr__(self):
		return '<Cage %r>' % (self.CageId)