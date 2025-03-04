from crud.crud_operations import (
    add_animal,
    get_all_animals,
    get_animal_by_id,
    update_animal,
    delete_animal,
)
from lesson import Lesson

# 1. Lisää uusi eläin
print("+ Lisätään eläin...")
animal_id = add_animal("Bertta", "Koira", "Sekarotuinen", "2025-02-14")
print(f"✅ Lisätty eläin ID: {animal_id}\n")

# 2. Haetaan kaikki eläimet
print("📋 Haetaan kaikki eläimet...")
animals = get_all_animals()
for animal in animals:
    print(animal)
print()

# 3. Haetaan eläin ID:n perusteella
print(f"🔍 Haetaan eläin ID: {2}...")
animal = get_animal_by_id(str(2))
print(animal, "\n")

# 4. Päivitetään eläin
print(f"✏️ Päivitetään eläin ID: {animal_id}...")
updated_animal = update_animal(
    animal_id, name="Siru", species="Koira", breed="Susikoira", birth_date="1990-01-01"
)
print(f"✅ Päivitetty eläin: {updated_animal}\n")

# 5. Poistetaan eläin
print(f"Poistetaan eläin ID: 3...")
deleted_id = delete_animal(animal_id="3")
print("Poistettu eläin ID:", deleted_id)

# 6. Haetaan kaikki ratsastustunnit
print("📋 Haetaan kaikki ratsastustunnit...")
lessons = Lesson.get_all_lessons()
for lesson in lessons:
    print(lesson)
print()
