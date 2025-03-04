from database import get_db_connection
from psycopg2.extras import RealDictCursor


def add_animal(name, species, breed=None, date_of_birth=None):
    if date_of_birth == "":
        date_of_birth = None
    if breed == "":
        breed = None

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO animal (name, species, breed, date_of_birth)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (name, species, breed, date_of_birth),
            )
            animal_id = cur.fetchone()[0]
            conn.commit()
            return animal_id


def get_all_animals():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM animal;")
            return cur.fetchall()


def get_animal_by_id(animal_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM animal WHERE animal_id = %s;", (animal_id,))
            return cur.fetchone()


def update_animal(animal_id, name=None, species=None, breed=None, date_of_birth=None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            fields = []
            values = []
            if name:
                fields.append("name = %s")
                values.append(name)
            if species:
                fields.append("species = %s")
                values.append(species)
            if breed:
                if breed == "":
                    breed = None
                fields.append("breed = %s")
                values.append(breed)
            if date_of_birth:
                fields.append("date_of_birth = %s")
                values.append(date_of_birth)

            values.append(animal_id)
            sql = f"UPDATE animal SET {', '.join(fields)} WHERE animal_id = %s RETURNING *;"
            cur.execute(sql, values)
            updated_animal = cur.fetchone()
            conn.commit()
            return updated_animal


def delete_animal(animal_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM animal WHERE animal_id = %s RETURNING animal_id;",
                (animal_id,),
            )
            deleted_id = cur.fetchone()
            conn.commit()
            return deleted_id


def get_animal_by_attribute(attribute):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            if attribute.isdigit():
                cur.execute("SELECT * FROM animal WHERE id = %s;", (attribute,))
            else:
                cur.execute("SELECT * FROM animal WHERE name = %s;", (attribute,))
            return cur.fetchone()
