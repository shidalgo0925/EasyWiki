import sqlite3

SQL = """CREATE TABLE IF NOT EXISTS coach_ai_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    api_provider VARCHAR(30) NOT NULL DEFAULT 'rules',
    use_custom_base_url BOOLEAN NOT NULL DEFAULT 0,
    base_url VARCHAR(500),
    api_key VARCHAR(500),
    model VARCHAR(120) NOT NULL DEFAULT 'gpt-4o-mini',
    context_window INTEGER NOT NULL DEFAULT 4096,
    request_timeout_ms INTEGER NOT NULL DEFAULT 180000,
    use_compact_prompt BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
)"""

if __name__ == "__main__":
    conn = sqlite3.connect("easycoach_dev.db")
    conn.execute(SQL)
    conn.execute("CREATE INDEX IF NOT EXISTS ix_coach_ai_configs_user_id ON coach_ai_configs (user_id)")
    conn.commit()
    conn.close()
    print("coach_ai_configs OK")
