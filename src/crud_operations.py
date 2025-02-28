import psycopg2.extras
from database import get_db_connection

# w


# 1. CREATE: Lisää uusi eläin
def add_animal(name, species, breed=None, birth_date=None):
    if birth_date == "":
        birth_date = None
    if breed == "":
        breed = None

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO animals (name, species, breed, birth_date)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """,
                (name, species, breed, birth_date),
            )
            animal_id = cur.fetchone()["id"]
            conn.commit()
            return animal_id


# READ
def get_all_animals():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM animals;")
            return cur.fetchall()


# READ
def get_animal_by_id(animal_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM animals WHERE id = %s;", (animal_id,))
            return cur.fetchone()


# READ
def get_all_lessons():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM lessons;")
            return cur.fetchall()


def get_animal_by_attribute(attr):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            if attr.isdigit():
                cur.execute("SELECT * FROM animals WHERE id = %s;", (int(attr),))
            elif attr.isalpha():
                attr = attr.lower()
                cur.execute("SELECT * FROM animals WHERE name = %s;", (attr,))
            else:
                print("Virheellinen arvo!")
                return None
            return cur.fetchone()


def get_available_horses():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            sql = f"SELECT * FROM animals WHERE species = 'horse'"
            cur.execute(sql)
            horses = cur.fetchall()
            return horses


def get_horse_by_name(name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            sql = f"SELECT * FROM animals WHERE name = %s"
            cur.execute(sql, (name,))
            return cur.fetchone()


def get_all_species(species):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            sql = f"SELECT * FROM animals WHERE species = %s;"
            cur.execute(sql, (species,))
            return cur.fetchall()


def update_animal(animal_id, name=None, species=None, breed=None, birth_date=None):
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
            if birth_date:

                fields.append("birth_date = %s")
                values.append(birth_date)

            values.append(animal_id)
            sql = f"UPDATE animals SET {', '.join(fields)} WHERE id = %s RETURNING *;"
            cur.execute(sql, values)
            updated_animal = cur.fetchone()
            conn.commit()
            return updated_animal


# 5. DELETE: Poista eläin
def delete_animal(animal_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM animals WHERE id = %s RETURNING id;", (animal_id,))
            deleted_id = cur.fetchone()
            conn.commit()
            return deleted_id
