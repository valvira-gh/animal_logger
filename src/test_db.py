from database import get_db_connection, init_db

def test_db_connection():
    try:
        init_db()  # Luo taulut
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()
                
                if result:
                    print(f"✅ Tietokantayhteys toimii! Tulos: {result}")
                else:
                    print("❌ Tietokantayhteys ei palauttanut tulosta!")

    except Exception as e:
        print(f"❌ Virhe tietokantayhteydessä: {e}")

if __name__ == "__main__":
    test_db_connection()
