import sqlite3
import json
from typing import Dict, Any, List
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)

class MemoryStore:
    def __init__(self, db_path: str = "jarvis_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                goal TEXT,
                observation TEXT,
                action TEXT,
                reflection TEXT,
                reward REAL,
                timestamp DATETIME
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS beliefs (
                id TEXT PRIMARY KEY,
                state TEXT,
                confidence REAL,
                updated DATETIME
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                pattern TEXT,
                reward REAL,
                usage INTEGER
            )
        ''')
        self.conn.commit()

    def save_episode(self, episode_data: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO episodes (id, goal, observation, action, reflection, reward, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            episode_data['id'],
            episode_data['goal'],
            json.dumps(episode_data['observation'], cls=DateTimeEncoder),
            json.dumps(episode_data['action'], cls=DateTimeEncoder),
            json.dumps(episode_data['reflection'], cls=DateTimeEncoder),
            episode_data['reward'],
            datetime.datetime.utcnow().isoformat()
        ))
        self.conn.commit()

    def update_belief(self, belief_id: str, state: Dict[str, Any], confidence: float):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO beliefs (id, state, confidence, updated)
            VALUES (?, ?, ?, ?)
        ''', (belief_id, json.dumps(state, cls=DateTimeEncoder), confidence, datetime.datetime.utcnow().isoformat()))
        self.conn.commit()

    def save_skill(self, skill_id: str, pattern: List[Dict[str, Any]], reward: float):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO skills (id, pattern, reward, usage)
            VALUES (?, ?, ?, COALESCE((SELECT usage FROM skills WHERE id = ?), 0) + 1)
        ''', (skill_id, json.dumps(pattern, cls=DateTimeEncoder), reward, skill_id))
        self.conn.commit()
