import pandas as pd
from crud_operations import add_animal, get_all_animals, get_all_species, get_animal_by_attribute
from database import init_db, delete_db
import time

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

    def add_lesson_flow(self):
        print()
        horses = get_all_species('Kissa')
        print(horses)
        
    
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



    def run(self):
        """Käyttösilmukka"""
        while self.running:
            self.show_menu()
            choice = input("\n⚡ Valitse toiminto: ")

            if choice == "1":
                print('\n' + 'LISÄÄ UUSI ELÄIN:')
                self.add_animal_flow() 
            elif choice == "2":
                print()
                self.get_all_animals_flow()
            elif choice == "3":
                print()
                self.get_animal_by_attr_flow()
            elif choice == "6":
                print()
                self.add_lesson_flow()
            elif choice == "x":
                print()
                confirm = input("Pyyhitäänkö tietokanta? (K/e) ")
                if confirm == "K":
                    self.delete_and_init_db_flow()
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