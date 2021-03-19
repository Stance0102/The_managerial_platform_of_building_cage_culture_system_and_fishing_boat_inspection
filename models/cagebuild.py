from sqlalchemy import Column, Integer, String, DateTime,Float
from database import Base
from sqlalchemy.orm import relationship
import uuid
import datetime

class Cagebuild(Base):
	__tablename__ = 'cagebuild'
	Id = Column(String(50),primary_key=True)
	CageClass = Column(String(50),nullable=True)
	BuildDate = Column(DateTime(),nullable=True)
	FixDate = Column(DateTime(),nullable=True)
	Lat = Column(Float(),nullable=True)
	Lng = Column(Float(),nullable=True)

	def __init__(self,CageClass,BuildDate,FixDate,Lat,Lng):
		self.Id = str(uuid.uuid4())
		self.CageClass = CageClass
		self.BuildDate = BuildDate
		self.FixDate = FixDate
		self.Lat = Lat
		self.Lng = Lng

	def __repr__(self):
		return '<Cage %r>' % (self.CageClass)