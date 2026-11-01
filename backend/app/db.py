from sqlalchemy import create_engine, text
from .config import settings

DATABASE_URL = settings.database_url or f"sqlite:///{settings.database_path}"
IS_SQLITE = DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if IS_SQLITE else {}
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)

def init_db():
    with engine.begin() as conn:
        if IS_SQLITE:
            conn.execute(text("PRAGMA foreign_keys=ON"))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL DEFAULT 'Nueva conversación',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(conversation_id) REFERENCES conversations(id)
                )
            """))
        else:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL DEFAULT 'Nueva conversación',
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS messages (
                    id BIGSERIAL PRIMARY KEY,
                    conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
                    role VARCHAR(20) NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, id)"))

def ensure_conversation(conversation_id: str):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO conversations(id) VALUES (:id) ON CONFLICT(id) DO NOTHING"),
            {"id": conversation_id}
        )

def add_message(conversation_id: str, role: str, content: str):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO messages(conversation_id, role, content) VALUES (:cid, :role, :content)"),
            {"cid": conversation_id, "role": role, "content": content}
        )
        conn.execute(
            text("UPDATE conversations SET updated_at=CURRENT_TIMESTAMP WHERE id=:id"),
            {"id": conversation_id}
        )

def get_messages(conversation_id: str, limit: int):
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT role, content FROM messages WHERE conversation_id=:cid ORDER BY id DESC LIMIT :lim"),
            {"cid": conversation_id, "lim": limit}
        ).mappings().all()
    return [dict(row) for row in reversed(rows)]

def list_conversations(limit: int = 50):
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC LIMIT :lim"),
            {"lim": limit}
        ).mappings().all()
    return [dict(row) for row in rows]
