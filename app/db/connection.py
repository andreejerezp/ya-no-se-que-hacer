import os
import time
from sqlalchemy import create_engine, text, URL
from sqlalchemy.exc import OperationalError


def build_database_url() -> str:
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_ROOT_PASSWORD", "")
    host = os.getenv("MYSQL_HOST", "db")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE", "caso1_parques_naturales")
    return URL.create(
        "mysql+pymysql",
        username=user,
        password=password,
        host=host,
        port=int(port),
        database=database,
        query={"charset": "utf8mb4"},
    )


engine = create_engine(build_database_url(), pool_pre_ping=True, pool_recycle=1800)


def wait_for_database(max_attempts: int = 30, delay_seconds: int = 2) -> None:
    """Wait until MySQL accepts a simple query; fail after bounded retries."""
    for attempt in range(1, max_attempts + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return
        except OperationalError:
            if attempt == max_attempts:
                raise
            time.sleep(delay_seconds)
