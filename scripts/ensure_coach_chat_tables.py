"""Create coach conversation tables."""
import sqlite3

SQL = [
    """CREATE TABLE IF NOT EXISTS coach_conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title VARCHAR(255),
        screen_context VARCHAR(100),
        activity_id INTEGER,
        provider_used VARCHAR(30),
        model_used VARCHAR(100),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS coach_chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_id INTEGER NOT NULL,
        role VARCHAR(20) NOT NULL,
        content TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(conversation_id) REFERENCES coach_conversations(id) ON DELETE CASCADE
    )""",
    "CREATE INDEX IF NOT EXISTS ix_coach_conversations_user_id ON coach_conversations (user_id)",
    "CREATE INDEX IF NOT EXISTS ix_coach_chat_messages_conversation_id ON coach_chat_messages (conversation_id)",
]

if __name__ == "__main__":
    conn = sqlite3.connect("easycoach_dev.db")
    for s in SQL:
        conn.execute(s)
    conn.commit()
    conn.close()
    print("Coach conversation tables OK")
