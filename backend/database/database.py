from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./mindmirror.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================================
# DATABASE MIGRATION
# =========================================================

def ensure_database():

    from database.models import User, Journal, ChatMessage

    Base.metadata.create_all(
        bind=engine
    )

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    if "chat_messages" in tables:

        columns = [
            column["name"]
            for column in inspector.get_columns(
                "chat_messages"
            )
        ]

        if "conversation_id" not in columns:

            with engine.begin() as connection:

                connection.execute(
                    text(
                        """
                        ALTER TABLE chat_messages
                        ADD COLUMN conversation_id VARCHAR
                        """
                    )
                )