from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    goal = Column(String)
    state = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    confidence = Column(Float)
    assistant_output = Column(String)
    repair_id = Column(Integer, ForeignKey('repair_history.id'), nullable=True)

class ToolHistory(Base):
    __tablename__ = 'tool_history'
    id = Column(Integer, primary_key=True)
    episode_id = Column(Integer, ForeignKey('episodes.id'))
    tool_name = Column(String)
    arguments = Column(JSON)
    result = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class RepairHistory(Base):
    __tablename__ = 'repair_history'
    id = Column(Integer, primary_key=True)
    original_episode_id = Column(Integer, ForeignKey('episodes.id'))
    error_message = Column(String)
    repair_action = Column(String)
    outcome = Column(String)

class Learning(Base):
    __tablename__ = 'learning'
    id = Column(Integer, primary_key=True)
    goal = Column(String)
    tool_used = Column(String)
    failure_reason = Column(String)
    repair_strategy = Column(String)
    outcome = Column(String)
    confidence_delta = Column(Float)
