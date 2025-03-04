from models import Animal


# Animal CRUD operations
def add_animal(conn, name, species, breed=None, date_of_birth=None):
    return Animal.create(conn, name, species, breed, date_of_birth)


def get_all_animals(conn):
    return Animal.get_all(conn)
