import sqlite3 as sqlt
from typing import Any


class Database:
    connection: sqlt.Connection
    db: sqlt.Cursor

    def __init__(self, name: str = "database.db", same_thread=True) -> None:
        self.connection = sqlt.connect(name, check_same_thread=same_thread)
        self.db = self.connection.cursor()

    def execute_one(self, sql: str) -> sqlt.Cursor:
        try:
            o = self.db.execute(sql)
            self.connection.commit()
            return o
        except sqlt.Error as e:
            print("Failed to execute query:\n", e)

    def fetch(self, sql: str, one=False, size=None) -> list[Any] | Any:
        try:
            o = None
            if one:
                o = self.db.execute(sql).fetchone()
                self.connection.commit()
                return o
            elif size:
                o = self.db.execute(sql).fetchmany(size)
                self.connection.commit()
                return o
            o = self.db.execute(sql).fetchall()
            self.connection.commit()
            return o
        except sqlt.Error as e:
            print("Failed to execute query:\n", e)

    def get_cols(self) -> list[str]:
        return [
            fld[1] for fld in self.db.execute(f"PRAGMA table_info(users);").fetchall()
        ]

    def close(self) -> None:
        self.db.close()


def init_db(db_name: str = "test") -> Database:
    db = Database(f"{db_name}.db", False)
    db.execute_one(
        """CREATE TABLE IF NOT EXISTS users (
          id VARCHAR(50) PRIMARY KEY NOT NULL,
          name VARCHAR(50) NOT NULL,
          email VARCHAR(50) NOT NULL,
          password VARCHAR(64) NOT NULL
        );
    """
    )
    return db
