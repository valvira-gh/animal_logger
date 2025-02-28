import pandas as pd
from crud_operations import (
    add_animal,
    get_all_animals,
    get_available_horses,
    get_horse_by_name,
    get_animal_by_attribute,
    update_animal,
    delete_animal,
    get_all_lessons,
)
from database import init_db, delete_db
from lesson import Lesson
import time
from datetime import datetime


class CLI:
    def __init__(self):
        """Alustetaan CLI"""
        self.running = True
        init_db()

    def show_menu(self):
        print("\n🐾 Animal Logger - Kotitilan eläinkirjanpito 🐾")
        print("1️⃣ Lisää uusi eläin")
        print("2️⃣ Näytä kaikki eläimet")
        print("3️⃣ Hae eläin nimen tai ID:n perusteella")
        print("4️⃣ Päivitä eläimen tiedot")
        print("5️⃣ Poista eläin")
        print("6️⃣ Lisää ratsastustunti")
        print("7️⃣ Näytä ratsastustunnit")
        print("0️⃣ Poistu")

    def add_animal_flow(self):
        species = ["horse", "dog", "cat", "sheep"]
        """Käyttäjän syötteet uuden eläimen lisäämiseen"""
        name = input("Nimi: ")
        index = int(input("(1) Hevonen, (2) Koira, (3) Kissa, (4) Lammas: "))
        breed = input("Rotu (valinnainen): ")
        birth_date = input("Eläimen arvioitu syntymäaika (YYYY-MM-DD, valinnainen): ")

        animal_id = add_animal(name, species[index - 1], breed, birth_date)
        print(f"✅ Added animal ID: {animal_id}) into a database!")

    def get_all_animals_flow(self):
        data = get_all_animals()
        df = pd.DataFrame(data)
        print(df)
        input("\n" + "Jatka painamalla näppäintä..." + "\n")

    def get_animal_by_attr_flow(self):
        input_attr = input("Anna eläimen nimi tai ID: ")
        animal = get_animal_by_attribute(input_attr)
        if animal:
            print()
            df = pd.DataFrame([animal])
            print(df)
        else:
            print("Eläintä ei löytynyt!")
        input("\n" + "Jatka painamalla näppäintä...")

    def print_all_lessons(self):
        print("\n" + "-" * 10 + "\n")
        print("KAIKKI RATSASTUSTUNNIT:" + "\n")
        lessons = get_all_lessons()
        df = pd.DataFrame(lessons)
        print(df)
        print()
        input("Paina näppäintä jatkaaksesi...")

    def add_lesson_flow(self):
        print("\n" + "-" * 10 + "\n")
        print("\n📅 LISÄÄ RATSASTUSTUNTI" + "\n")
        horses = get_available_horses()
        self.print_available_horses(horses)
        horse_id = self.get_horse_id_from_user(horses)
        rider = input("Ratsastaja: ")
        date = self.get_date_from_user()
        duration = float(input("Kesto (tunnit, desimaaliluku): "))
        fare = int(input("Hinta (yhdeltä tunnilta): "))
        notes = input("Muistiinpanot (valinnainen): ")

        lesson = Lesson(horse_id, rider, date, duration, fare, notes)
        lesson_id = lesson.save_to_db()
        print(f"✅ Ratsastustunti ID: {lesson_id} lisätty tietokantaan!")

    def get_date_from_user(self):
        while True:
            date = input("Päivämäärä (YYYY-MM-DD): ")
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Virheellinen päivämäärä, yritä uudestaan.")

        return date

    def print_available_horses(self, horses):
        df = pd.DataFrame(horses)
        df = df.drop(columns=["birth_date", "created_at"])

        print(df.to_string(index=False))

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
        print()
        while True:
            try:
                id = int(input("Anna päivitettävän eläimen ID: "))
                break
            except ValueError:
                print("Virheellinen ID, yritä uudelleen.")

        name = input("Uusi nimi (jätä tyhjäksi jos ei muutosta): ")
        species = input("Uusi laji (jätä tyhjäksi jos ei muutosta): ")
        breed = input("Uusi rotu (jätä tyhjäksi jos ei muutosta): ")
        birth_date = input(
            "Uusi syntymäaika (YYYY-MM-DD, jätä tyhjäksi jos ei muutosta): "
        )

        updated_animal = update_animal(id, name, species, breed, birth_date)
        if updated_animal:
            print()
            print(f"✅ Eläimen ID {id} tiedot päivitetty!")
        else:
            print()
            print(f"❌ Eläimen ID {id} päivitys epäonnistui!")

    def delete_animal_flow(self):
        print()
        while True:
            try:
                id = int(input("Anna poistettavan eläimen ID: "))
                break
            except ValueError:
                print()
                print("Virheellinen ID, yritä uudestaan...")
        deleted_id = delete_animal(id)
        print()
        print(f"Eläin ID {id} poistettiin onnistuneesti tietokannasta!")

    def run(self):
        """Käyttösilmukka"""
        while self.running:
            self.show_menu()
            choice = input("\n⚡ Valitse toiminto: ")

            if choice == "1":
                print("\n" + "LISÄÄ UUSI ELÄIN:")
                self.add_animal_flow()
            elif choice == "2":
                print()
                self.get_all_animals_flow()
            elif choice == "3":
                print()
                self.get_animal_by_attr_flow()
            elif choice == "4":
                print()
                self.update_animal_flow()
            elif choice == "5":
                print()
                self.delete_animal_flow()
                input("Jatka painamalla näppäintä...")
            elif choice == "6":
                print()
                self.add_lesson_flow()
            elif choice == "7":
                print()
                self.print_all_lessons()
            elif choice == "x":
                print()
                confirm = input("Pyyhitäänkö tietokanta? (K/e) ")
                if confirm == "K":
                    self.delete_and_init_db()
                elif confirm.lower() == "e":
                    pass

            elif choice == "0":
                print("👋 Suljetaan sovellus...")
                self.running = False
            else:
                print("❌ Virheellinen valinta, yritä uudelleen.")


if __name__ == "__main__":
    cli = CLI()
    cli.run()
