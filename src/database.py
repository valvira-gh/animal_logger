import psycopg2

DATABASE_URL = (
    "dbname=animal_logger user=postgres password=dbpassword host=localhost port=5432"
)


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Luo tietokantataulut puhtaalla SQL:llä"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS animal (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    species VARCHAR(50) NOT NULL,
                    breed VARCHAR(100),
                    date_of_birth DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS horse (
                    id SERIAL PRIMARY KEY,
                    animal_id INTEGER NOT NULL,
                    is_available BOOLEAN NOT NULL,
                    training_level INTEGER CHECK (training_level BETWEEN 0 AND 3),
                    FOREIGN KEY (animal_id) REFERENCES animal (id) ON DELETE CASCADE
                );
                """
            )
            conn.commit()


def delete_db():
    """Poistaa taulut 'horse' ja 'animal'"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS horse;")
            cur.execute("DROP TABLE IF EXISTS animal;")
            conn.commit()
