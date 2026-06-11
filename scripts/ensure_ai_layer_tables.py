"""Migración incremental capa IA."""
import sqlite3

conn = sqlite3.connect("easycoach_dev.db")
cur = conn.cursor()

def col_exists(table, col):
    cur.execute(f"PRAGMA table_info({table})")
    return col in [r[1] for r in cur.fetchall()]

def add_col(table, col, typedef):
    if not col_exists(table, col):
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typedef}")
        print(f"  + {table}.{col}")

add_col("coach_conversations", "source", "VARCHAR(50)")
add_col("coach_conversations", "treatment_id", "INTEGER")
add_col("coach_chat_messages", "user_id", "INTEGER")
add_col("coach_chat_messages", "provider", "VARCHAR(30)")
add_col("coach_chat_messages", "model", "VARCHAR(100)")
add_col("coach_chat_messages", "latency_ms", "INTEGER DEFAULT 0")
add_col("coach_chat_messages", "tokens_input", "INTEGER DEFAULT 0")
add_col("coach_chat_messages", "tokens_output", "INTEGER DEFAULT 0")
add_col("coach_chat_messages", "error_code", "VARCHAR(100)")

cur.execute("""CREATE TABLE IF NOT EXISTS coach_ai_call_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    provider VARCHAR(30),
    model VARCHAR(100),
    latency_ms INTEGER DEFAULT 0,
    tokens_input INTEGER DEFAULT 0,
    tokens_output INTEGER DEFAULT 0,
    source VARCHAR(50),
    success BOOLEAN DEFAULT 0,
    error_code VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)""")
cur.execute("CREATE INDEX IF NOT EXISTS ix_coach_ai_call_logs_user_id ON coach_ai_call_logs (user_id)")

conn.commit()
conn.close()
print("AI layer tables OK")
