import pandas as pd
from crud.crud_operations import (
    add_animal,
    get_all_animals,
    update_animal,
    delete_animal,
    get_animal_by_attribute,
)
from database import init_db, delete_db, get_db_connection
from lesson import Lesson
import time
from datetime import datetime
from models.horse import Horse


class CLI:
    def __init__(self):
        """Alustetaan CLI"""
        self.running = True
        init_db()

    def show_main_menu(self):
        print("\n🐾 Animal Logger - Kotitilan eläinkirjanpito 🐾")
        print("1️⃣ Eläimet")
        print("2️⃣ Ratsastustunnit")
        print("0️⃣ Poistu")

    def show_animal_menu(self):
        print("\n🐾 Eläimet 🐾")
        print("1️⃣ Lisää uusi eläin")
        print("2️⃣ Näytä kaikki eläimet")
        print("3️⃣ Hae eläin nimen tai ID:n perusteella")
        print("4️⃣ Päivitä eläimen tiedot")
        print("5️⃣ Poista eläin")
        print("0️⃣ Palaa takaisin")

    def show_lesson_menu(self):
        print("\n🐾 Ratsastustunnit 🐾")
        print("1️⃣ Lisää ratsastustunti")
        print("2️⃣ Näytä ratsastustunnit")
        print("0️⃣ Palaa takaisin")

    def add_animal_flow(self):
        self.print_line()
        species = ["horse", "dog", "cat", "sheep"]
        """Käyttäjän syötteet uuden eläimen lisäämiseen"""
        name = input("Nimi: ")
        index = self.get_valid_input(
            "(1) Hevonen, (2) Koira, (3) Kissa, (4) Lammas: ", int, range(1, 5)
        )
        breed = input("Rotu (valinnainen): ")
        date_of_birth = input(
            "Eläimen arvioitu syntymäaika (YYYY-MM-DD, valinnainen): "
        )

        if species[index - 1] == "horse":
            with get_db_connection() as conn:
                horse = Horse.create(conn, name, breed, date_of_birth)
                print(f"✅ Added horse ID: {horse.animal_id} into a database!")
        else:
            animal_id = add_animal(name, species[index - 1], breed, date_of_birth)
            print(f"✅ Added animal ID: {animal_id}) into a database!")

    def get_all_animals_flow(self):
        self.print_line()
        data = get_all_animals()
        self.print_dataframe(data)

    def get_animal_by_attr_flow(self):
        self.print_line()
        input_attr = input("Anna eläimen nimi tai ID: ")
        animal = get_animal_by_attribute(input_attr)
        if animal:
            self.print_dataframe([animal])
        else:
            print("Eläintä ei löytynyt!")
        input("\n" + "Jatka painamalla näppäintä...")

    def print_all_lessons(self):
        self.print_line()
        print("KAIKKI RATSASTUSTUNNIT:" + "\n")
        lessons = Lesson.get_all_lessons()
        self.print_dataframe(lessons)

    def add_lesson_flow(self):
        self.print_line()
        print("\n📅 LISÄÄ RATSASTUSTUNTI" + "\n")

        with get_db_connection() as conn:
            horses = Horse.get_available_horses(conn)
        print("Available horses:\n", horses)

        horse_id = self.get_horse_id_from_user(horses)
        rider = input("Ratsastaja: ")
        date = self.get_date_from_user()
        duration = self.get_valid_input("Kesto (tunnit, desimaaliluku): ", float)
        fare = self.get_valid_input("Hinta (yhdeltä tunnilta): ", int)
        notes = input("Muistiinpanot (valinnainen): ")

        lesson = Lesson(horse_id, rider, date, duration, fare, notes)
        lesson_id = lesson.save_to_db()
        print(f"✅ Ratsastustunti ID: {lesson_id} lisätty tietokantaan!")

    def get_date_from_user(self):
        while True:
            date = input("Päivämäärä (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                return date
            except ValueError:
                print("Virheellinen päivämäärä, yritä uudestaan.")

    def get_horse_id_from_user(self, horses: list[tuple]):
        horse_dict = {horse["name"]: horse["id"] for horse in horses}
        while True:
            print()
            selection = input("Anna hevosen nimi tai ID: ")
            if selection.isdigit():
                id = int(selection)
                if id in [horse["id"] for horse in horses]:
                    return id
                else:
                    print("Virheellinen ID, yritä uudelleen.")
            elif selection in horse_dict:
                return horse_dict[selection]
            else:
                print("Virheellinen nimi, yritä uudelleen.")

    def delete_and_init_db_flow(self):
        print("Pyyhitään tietokanta...")
        time.sleep(0.5)
        delete_db()
        print("Tietokanta pyyhitty! (1/2)")
        print("Alustetaan tietokanta...")
        time.sleep(0.5)
        init_db()
        print("Tietokanta alustettu! (2/2)")
        time.sleep(1)

    def update_animal_flow(self):
        self.print_line()
        id = self.get_valid_input("Anna päivitettävän eläimen ID: ", int)
        name = input("Uusi nimi (jätä tyhjäksi jos ei muutosta): ")
        species = input("Uusi laji (jätä tyhjäksi jos ei muutosta): ")
        breed = input("Uusi rotu (jätä tyhjäksi jos ei muutosta): ")
        date_of_birth = input(
            "Uusi syntymäaika (YYYY-MM-DD, jätä tyhjäksi jos ei muutosta): "
        )

        updated_animal = update_animal(id, name, species, breed, date_of_birth)
        if updated_animal:
            print(f"✅ Eläimen ID {id} tiedot päivitetty!")
        else:
            print(f"❌ Eläimen ID {id} päivitys epäonnistui!")

    def delete_animal_flow(self):
        self.print_line()
        id = self.get_valid_input("Anna poistettavan eläimen ID: ", int)
        deleted_id = delete_animal(id)
        print(f"Eläin ID {id} poistettiin onnistuneesti tietokannasta!")

    @staticmethod
    def print_line():
        print()
        print("-" * 10)
        print()

    @staticmethod
    def print_dataframe(data):
        df = pd.DataFrame(data)
        print(df)
        input("\n" + "Jatka painamalla näppäintä..." + "\n")

    def get_valid_input(self, prompt, input_type, valid_range=None):
        while True:
            try:
                value = input_type(input(prompt))
                if valid_range and value not in valid_range:
                    raise ValueError
                return value
            except ValueError:
                print("Virheellinen syöte, yritä uudelleen.")

    def run(self):
        while self.running:
            self.show_main_menu()
            choice = input("\n⚡ Valitse toiminto: ")

            if choice == "1":
                while True:
                    self.print_line()
                    self.show_animal_menu()
                    animal_choice = input("\n⚡ Valitse toiminto: ")
                    if animal_choice == "1":
                        self.add_animal_flow()
                    elif animal_choice == "2":
                        self.get_all_animals_flow()
                    elif animal_choice == "3":
                        self.get_animal_by_attr_flow()
                    elif animal_choice == "4":
                        self.update_animal_flow()
                    elif animal_choice == "5":
                        self.delete_animal_flow()
                        input("Jatka painamalla näppäintä...")
                    elif animal_choice == "0":
                        break
                    else:
                        print("❌ Virheellinen valinta, yritä uudelleen.")

            elif choice == "2":
                while True:
                    self.print_line()
                    self.show_lesson_menu()
                    lesson_choice = input("\n⚡ Valitse toiminto: ")
                    if lesson_choice == "1":
                        self.add_lesson_flow()
                    elif lesson_choice == "2":
                        self.print_all_lessons()
                    elif lesson_choice == "0":
                        break
                    else:
                        print("❌ Virheellinen valinta, yritä uudelleen.")

            elif choice == "0":
                print("👋 Suljetaan sovellus...")
                self.running = False
            else:
                print("❌ Virheellinen valinta, yritä uudelleen.")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
