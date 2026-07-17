import psycopg2
from config import DB_CONFIG


def get_connection():
    """Create and return a PostgreSQL connection."""

    try:
        connection = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )

        print("Connected to PostgreSQL successfully!")

        return connection

    except Exception as e:
        print(f"Database connection failed: {e}")
        return None