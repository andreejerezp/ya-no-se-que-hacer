from sqlalchemy import text
from .connection import engine



def count_visitors() -> int:
    """Return the number of rows in the real DDL table VISITANTE."""
    with engine.connect() as connection:
        return int(connection.execute(text("SELECT COUNT(*) FROM VISITANTE")).scalar_one())


def count_excursions() -> int:
    """Return the number of rows in the real DDL table EXCURSION."""
    with engine.connect() as connection:
        return int(connection.execute(text("SELECT COUNT(*) FROM EXCURSION")).scalar_one())
