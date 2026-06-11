"""Create coach live tables if missing."""
import sqlite3

TABLES = [
    """CREATE TABLE IF NOT EXISTS coach_activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        objective TEXT,
        project_key VARCHAR(100),
        priority INTEGER NOT NULL DEFAULT 2,
        scheduled_date DATE,
        scheduled_start_time TIME,
        scheduled_end_time TIME,
        estimated_minutes INTEGER NOT NULL DEFAULT 30,
        status VARCHAR(20) NOT NULL DEFAULT 'draft',
        current_step_id INTEGER,
        last_interaction_at DATETIME,
        ai_context TEXT,
        ai_recommendation TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS coach_activity_steps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_id INTEGER NOT NULL,
        step_order INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        expected_output TEXT,
        status VARCHAR(20) NOT NULL DEFAULT 'pending',
        user_input_required BOOLEAN NOT NULL DEFAULT 0,
        user_response TEXT,
        completed_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(activity_id) REFERENCES coach_activities(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS coach_work_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        activity_id INTEGER NOT NULL,
        started_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        paused_at DATETIME,
        completed_at DATETIME,
        status VARCHAR(20) NOT NULL DEFAULT 'active',
        current_step_id INTEGER,
        session_notes TEXT,
        ai_summary TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(activity_id) REFERENCES coach_activities(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS coach_habit_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        habit_type VARCHAR(30) NOT NULL,
        title VARCHAR(100) NOT NULL,
        message TEXT NOT NULL,
        preferred_time TIME,
        interval_minutes INTEGER,
        enabled BOOLEAN NOT NULL DEFAULT 1,
        last_triggered_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS coach_daily_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        current_mode VARCHAR(30) NOT NULL DEFAULT 'normal',
        energy_level INTEGER,
        focus_score INTEGER,
        agenda_summary TEXT,
        active_activity_id INTEGER,
        next_recommendation TEXT,
        daily_close_done BOOLEAN NOT NULL DEFAULT 0,
        last_water_at DATETIME,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""",
    """CREATE TABLE IF NOT EXISTS coach_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        msg_type VARCHAR(20) NOT NULL DEFAULT 'info',
        message TEXT NOT NULL,
        suggested_action VARCHAR(255),
        action_url VARCHAR(255),
        is_read BOOLEAN NOT NULL DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    )""",
]

INDEXES = [
    "CREATE INDEX IF NOT EXISTS ix_coach_activities_user_id ON coach_activities (user_id)",
    "CREATE INDEX IF NOT EXISTS ix_coach_activity_steps_activity_id ON coach_activity_steps (activity_id)",
    "CREATE INDEX IF NOT EXISTS ix_coach_work_sessions_user_id ON coach_work_sessions (user_id)",
]

if __name__ == "__main__":
    conn = sqlite3.connect("easycoach_dev.db")
    cur = conn.cursor()
    for sql in TABLES:
        cur.execute(sql)
    for sql in INDEXES:
        cur.execute(sql)
    conn.commit()
    conn.close()
    print("Coach live tables OK")
