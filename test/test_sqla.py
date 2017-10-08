#!/usr/bin/env python3

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
 
Base = declarative_base()

class Task(Base):
    id = Column(Integer, primary_key=True)
    result = Column(String)
    name = Column(String)
    cmdline = Column(String)
    
