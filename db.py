# Conexão SQLite + DAO
import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple
from zoneinfo import ZoneInfo

# Fusos horários
TZ_UTC = ZoneInfo("UTC")
TZ_SP = ZoneInfo("America/Sao_Paulo")

DB_PATH = "chatbot.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_schema():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        user_msg TEXT NOT NULL,
        bot_msg  TEXT NOT NULL,
        sentiment TEXT,
        intent TEXT,
        is_crisis INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS safety_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        user_msg TEXT NOT NULL,
        matched_pattern TEXT,
        created_at TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def save_turn(user_id: str, user_msg: str, bot_msg: str,
              sentiment: Optional[str], intent: Optional[str], is_crisis: int):
    """Salva mensagem com horário de SP no banco"""
    created_at = datetime.now(TZ_SP).isoformat()  # grava já no fuso correto
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO conversations (user_id, user_msg, bot_msg, sentiment, 
                intent, is_crisis, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (user_id, user_msg, bot_msg, sentiment, intent, is_crisis, created_at))
    conn.commit()
    conn.close()

def log_safety(user_id: str, user_msg: str, matched_pattern: str):
    """Loga mensagens de crise com horário de SP"""
    created_at = datetime.now(TZ_SP).isoformat()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO safety_logs (user_id, user_msg, matched_pattern, created_at)
        VALUES (?, ?, ?, ?);
    """, (user_id, user_msg, matched_pattern, created_at))
    conn.commit()
    conn.close()

def last_messages(limit: int = 10) -> List[Tuple]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_msg, bot_msg, created_at FROM conversations
        ORDER BY id ASC LIMIT ?;
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

