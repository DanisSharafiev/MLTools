import psycopg2
from psycopg2.extras import RealDictCursor
import os

class PostgresClient:
    def __init__(
        self,
        host: str = os.getenv("DB_HOST", "localhost"),
        port: int = int(os.getenv("DB_PORT", "5432")),
        user: str = os.getenv("DB_USER", "mock"),
        password: str = os.getenv("DB_PASSWORD", "mock"),
        database: str = os.getenv("DB_NAME", "mock")
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
    
    def connect(self):
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        return self.conn
    
    def execute_query(self, query : str, params : tuple = ()):
        conn = self.conn
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if cursor.description:
                return cursor.fetchall()
            conn.commit()
            return []
    
    # Could be done with a SQLModel

    def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS files (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL
        );
        """
        self.execute_query(query)
        query = """
        CREATE TABLE IF NOT EXISTS models (
            id SERIAL PRIMARY KEY,
            file_name VARCHAR(255) NOT NULL,
            features VARCHAR(255) NOT NULL,
            target VARCHAR(255) NOT NULL,
            model_type VARCHAR(255) NOT NULL,
        );
        """
        self.execute_query(query)

    def select_file(self, file_name: str):
        query = "SELECT * FROM files WHERE name = %s"
        return self.execute_query(query, (file_name,))
    
    def select_all_files(self):
        query = "SELECT * FROM files"
        return self.execute_query(query)

    def close(self):
        if self.conn is not None:
            self.conn.close()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()