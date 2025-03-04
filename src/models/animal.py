import psycopg2
from psycopg2.extras import RealDictCursor


class Animal:
    def __init__(
        self, id, name, species, breed=None, date_of_birth=None, created_at=None
    ):
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.date_of_birth = date_of_birth
        self.created_at = created_at

    @staticmethod
    def create(conn, name, species, breed=None, date_of_birth=None):
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO animal (name, species, breed, date_of_birth)
                VALUES (%s, %s, %s, %s)
                RETURNING id, created_at
                """,
                (name, species, breed, date_of_birth),
            )
            id, created_at = cur.fetchone()
        return Animal(id, name, species, breed, date_of_birth, created_at)

    @staticmethod
    def get_all(conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM animal")
            rows = cur.fetchall()
        return [Animal(**row) for row in rows]

    @staticmethod
    def get_by_id(conn, id):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM animal WHERE id = %s", (id,))
            row = cur.fetchone()
        if row:
            return Animal(**row)
        return None

    @staticmethod
    def update(conn, id, **kwargs):
        set_clause = ", ".join([f"{key} = %s" for key in kwargs])
        values = list(kwargs.values()) + [id]
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE animal SET {set_clause} WHERE id = %s;", values)
            conn.commit()

    @staticmethod
    def delete(conn, id):
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM animal WHERE id = %s;", (id,))
            conn.commit()
