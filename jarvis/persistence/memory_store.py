from sqlalchemy import create_engine, Column, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
import json
from typing import Dict, Any, List

Base = declarative_base()

class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(String, primary_key=True)
    goal = Column(String)
    observation = Column(Text)
    action = Column(Text)
    reflection = Column(Text)
    reward = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Belief(Base):
    __tablename__ = 'beliefs'
    id = Column(String, primary_key=True)
    state = Column(Text)
    confidence = Column(Float)
    updated = Column(DateTime, default=datetime.datetime.utcnow)

class MemoryStore:
    def __init__(self, db_url: str = "sqlite:///jarvis_memory.db"):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def save_episode(self, data: dict):
        session = self.Session()
        try:
            episode = Episode(
                id=data['id'],
                goal=data['goal'],
                observation=json.dumps(data['observation']),
                action=json.dumps(data['action']),
                reflection=json.dumps(data['reflection']),
                reward=data['reward']
            )
            session.add(episode)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def update_belief(self, belief_id: str, state: dict, confidence: float):
        session = self.Session()
        try:
            belief = session.query(Belief).filter_by(id=belief_id).first()
            if belief:
                belief.state = json.dumps(state)
                belief.confidence = confidence
                belief.updated = datetime.datetime.utcnow()
            else:
                belief = Belief(id=belief_id, state=json.dumps(state), confidence=confidence)
                session.add(belief)
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def get_recent_episodes(self, limit: int = 20) -> List[Dict[str, Any]]:
        session = self.Session()
        try:
            episodes = session.query(Episode).order_by(Episode.timestamp.desc()).limit(limit).all()
            return [{
                "id": e.id,
                "goal": e.goal,
                "reward": e.reward,
                "timestamp": e.timestamp.isoformat()
            } for e in episodes]
        finally:
            self.Session.remove()

    def get_beliefs(self) -> List[Dict[str, Any]]:
        session = self.Session()
        try:
            beliefs = session.query(Belief).all()
            return [{
                "id": b.id,
                "confidence": b.confidence,
                "updated": b.updated.isoformat()
            } for b in beliefs]
        finally:
            self.Session.remove()

    def summarize(self):
        session = self.Session()
        try:
            count = session.query(Episode).count()
            return {"episode_count": count}
        finally:
            self.Session.remove()

    def compact(self):
        with self.engine.connect() as conn:
            conn.execute("VACUUM")
