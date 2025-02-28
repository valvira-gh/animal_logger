from database import get_db_connection


class Lesson:
    def __init__(self, horse_id, rider_name, date, duration, fare, notes=None):
        self.horse_id = horse_id
        self.rider_name = rider_name
        self.date = date
        self.duration = duration
        self.fare = fare
        self.notes = notes

    def init_lessons_table(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        CREATE TABLE IF NOT EXISTS lessons (
                                id SERIAL PRIMARY KEY,
                                horse_id INT REFERENCES animals(id) ON DELETE CASCADE,
                                rider_name VARCHAR(100) NOT NULL,
                                date DATE NOT NULL,
                                duration FLOAT NOT NULL,
                                fare INT NOT NULL,
                                notes TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                """
                )
                conn.commit()

    def save_to_db(self):
        """Saves the riding lesson to the database."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO lessons (horse_id, rider_name, date, duration, fare, notes)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
                """,
                    (
                        self.horse_id,
                        self.rider_name,
                        self.date,
                        self.duration,
                        self.fare,
                        self.notes,
                    ),
                )
                lesson_id = cur.fetchone()["id"]
                conn.commit()
                return lesson_id

    @staticmethod
    def get_all_lessons():
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM lessons;")
                return cur.fetchall()

    @staticmethod
    def get_lesson_by_id(lesson_id):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM lessons WHERE id = %s;", (lesson_id,))
                return cur.fetchone()


if __name__ == "__main__":
    test_lesson = Lesson(4, "Tarmo Testaaja", "2025-02-25", 2.5, 20)
    test_lesson.init_lessons_table()
    # test_lesson.save_to_db()
    # all_lessons = test_lesson.get_all_lessons()
    # print("All:", all_lessons)
    # by_id = test_lesson.get_lesson_by_id(2)
    # print("By id:", by_id)
    pass
