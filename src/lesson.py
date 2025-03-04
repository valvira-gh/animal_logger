from database import get_db_connection
from psycopg2.extras import RealDictCursor
import pandas as pd


class Lesson:
    def __init__(
        self,
        horse_id=None,
        rider_name=None,
        date=None,
        duration=None,
        fare=None,
        notes=None,
    ):
        self.horse_id = horse_id
        self.rider_name = rider_name
        self.date = date
        self.duration = duration
        self.fare = fare
        self.notes = notes

    def save_to_db(self):
        """Saves the riding lesson to the database."""
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
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
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM lessons;")
                return cur.fetchall()

    @staticmethod
    def get_lesson_by_id(lesson_id):
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM lessons WHERE id = %s;", (lesson_id,))
                return cur.fetchone()

    @staticmethod
    def get_available_horses():
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, name, species, breed FROM animal WHERE species='horse';"
                )
                return cur.fetchall()


if __name__ == "__main__":
    test_lesson = Lesson()
    available_horses = test_lesson.get_available_horses()
    print("Available horses:\n", available_horses)
    # test_lesson.save_to_db()
    # all_lessons = test_lesson.get_all_lessons()
    # print("All:", all_lessons)
    # by_id = test_lesson.get_lesson_by_id(2)
    # print("By id:", by_id)
    pass
