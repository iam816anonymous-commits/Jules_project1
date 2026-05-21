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
        self.db_path = db_path
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

    def archive(self, days: int = 30):
        """Move old episodes to archive table or separate DB."""
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS archived_episodes AS SELECT * FROM episodes WHERE 1=0")
        cursor.execute("INSERT INTO archived_episodes SELECT * FROM episodes WHERE timestamp < datetime('now', ?)", (f'-{days} days',))
        cursor.execute("DELETE FROM episodes WHERE timestamp < datetime('now', ?)", (f'-{days} days',))
        self.conn.commit()

    def compact(self):
        """Reclaim unused space."""
        self.conn.execute("VACUUM")

    def summarize(self) -> Dict[str, Any]:
        """Performance summary of the DB."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM episodes")
        count = cursor.fetchone()[0]
        import os
        size = os.path.getsize(self.db_path) / (1024 * 1024) # MB
        return {"episode_count": count, "db_size_mb": size}
