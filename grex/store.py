#!/usr/bin/env python3
'''
Database store.
'''

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
 
import sqlalchemy.types as types
import json


# https://avacariu.me/articles/2016/compiling-json-as-text-for-sqlite-with-sqlalchemy
import sqlalchemy.types as types
class StringyJSON(types.TypeDecorator):
    """Stores and retrieves JSON as TEXT."""
    impl = types.TEXT
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value
    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
JSON = types.JSON().with_variant(StringyJSON, 'sqlite')


Base = declarative_base()

class DaqRun(Base):
    '''
    Information about one data aquisition result.
    '''

    __tablename__ = "daqrun"

    id = Column(Integer, primary_key=True)
    host = Column(String)
    category = Column(String)
    config = Column(String)
    timestamp = Column(String)
    datadir = Column(String)

    stages = relationship("Stages", back_populates="daqrun")

    def ident(self):
        keys = 'host category config timestamp'.split()
        return '-'.join([getattr(self, key) for key in keys])
    def __repr__(self):
        return self.ident()
    def asdict(self):
        d = dict(self.__dict__)
        d.pop('_sa_instance_state')
        d['ident'] = self.ident()
        d['stages'] = [s.name for s in self.stages]
        return d

class Stages(Base):
    '''
    Record what as been done to a data aquistion result
    '''
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    command = Column(String)       # instance independent desc of what this stage does
    params = Column(JSON)
    result = Column(JSON)
    
    daqrun_id = Column(Integer, ForeignKey('daqrun.id'))
    daqrun = relationship("DaqRun", back_populates="stages")

    def __repr__(self):
        return "<Stage {}: {}>".format(self.name, self.daqrun.ident())

    def __hash__(self):
        return hash((self.command, self.daqrun_id, self.params))


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def session(dburl="sqlite:///:memory:"):
    '''
    Return a DB session
    '''
    engine = create_engine(dburl)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
    
