import os

from sqlalchemy import (
    create_engine,
    inspect,
    text
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


# =========================================================
# DATABASE URL
# =========================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./mindmirror.db"
)


# =========================================================
# POSTGRES URL COMPATIBILITY
# =========================================================

if DATABASE_URL.startswith(
    "postgres://"
):

    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


# =========================================================
# ENGINE
# =========================================================

engine_options = {}


if DATABASE_URL.startswith(
    "sqlite"
):

    engine_options[
        "connect_args"
    ] = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    **engine_options
)


# =========================================================
# SESSION
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


# =========================================================
# DATABASE DEPENDENCY
# =========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================================
# DATABASE SETUP
# =========================================================

def ensure_database():

    # Models are imported by main.py before this
    # function runs, so SQLAlchemy already knows
    # about the registered tables.

    Base.metadata.create_all(
        bind=engine
    )


    # =====================================================
    # LEGACY SQLITE MIGRATION
    # =====================================================

    # This migration only exists for older local databases.
    # Production databases created from the current models
    # already contain conversation_id.

    if not DATABASE_URL.startswith(
        "sqlite"
    ):

        return


    inspector = inspect(
        engine
    )


    tables = (
        inspector.get_table_names()
    )


    if "chat_messages" not in tables:

        return


    columns = [

        column["name"]

        for column
        in inspector.get_columns(
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