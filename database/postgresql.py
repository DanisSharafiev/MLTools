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
        
    def close(self):
        if self.conn is not None:
            self.conn.close()
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()