from models.animal import Animal


class Horse(Animal):
    def __init__(
        self,
        id=None,
        name=None,
        species="horse",
        breed=None,
        date_of_birth=None,
        is_available=None,
        training_level=None,
        created_at=None,
    ):
        super().__init__(id, name, species, breed, date_of_birth, created_at)
        self.is_available = is_available
        self.training_level = training_level

    @staticmethod
    def create(
        conn,
        name,
        breed=None,
        date_of_birth=None,
    ):
        is_available = (
            input("Onko hevonen käytettävissä opetuskäyttöön (kyllä/ei):  ")
            .strip()
            .lower()
            == "kyllä"
        )
        training_level = int(input("Koulutustaso (0 - 3): "))

        if date_of_birth == "":
            date_of_birth = None

        animal = Animal.create(conn, name, "horse", breed, date_of_birth)
        horse = Horse(
            id=animal.id,
            name=name,
            species="horse",
            breed=breed,
            date_of_birth=date_of_birth,
            is_available=is_available,
            training_level=training_level,
            created_at=animal.created_at,
        )

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO horse (animal_id, is_available, training_level)
                VALUES (%s, %s, %s)
                """,
                (horse.id, horse.is_available, horse.training_level),
            )
        return horse

    @staticmethod
    def get_all(conn):
        animals = Animal.get_all(conn)
        return [
            Horse(**animal.__dict__) for animal in animals if animal.species == "horse"
        ]

    @staticmethod
    def get_by_id(conn, id):
        animal = Animal.get_by_id(conn, id)
        if animal and animal.species == "horse":
            return Horse(**animal.__dict__)
        return None

    @staticmethod
    def get_available_horses(conn):
        all_horses = Horse.get_all(conn)
        available_horses = [horse for horse in all_horses if horse.is_available]
        return available_horses
