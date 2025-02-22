import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "dbname=animal_logger user=postgres password=dbpassword host=localhost port=5432"

def get_db_connection():
    """Avaa psycopg2-tietokantayhteyden"""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_db():
    """Luo tietokantataulut puhtaalla SQL:llä"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS animals (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    species VARCHAR(50) NOT NULL,
                    breed VARCHAR(100),
                    birth_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()


def delete_db():
    """Poistaa taulun 'animals'"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE animals;")
            conn.commit()
