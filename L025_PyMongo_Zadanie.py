from pymongo import MongoClient
import pymongo
import re
from pprint import pprint

# tworzenie połączenia
client = MongoClient()

# wybór bazy danych
db = client.test

def menu_func():
    print('''Menu:
    1. Wyszukiwanie restauracji po ID
    2. Wyszukiwanie restauracji po kodzie pocztowym
    3. Wyszukiwanie restauracji po nazwie
    4. Wyszukiwanie restauracji w twojej okolicy
    5. Wyszukiwanie restauracji serwującej zadaną kuchnię
    6. Wyszukiwanie restauracji w obrębie dzielnicy, TOP X''')

    try:
        choose = int(input('Wybierz interesującą Cie opcję: '))
    except ValueError:
        raise ValueError('Poadana wartość musi być cyfrą!')
    if choose not in (1,2,3,4,5,6):
        raise ValueError('Poadana wartość musi być cyfrą od 1 do 6!')

    return choose

def connection_with_db():
    client = MongoClient()
    db = client.test
    collection = db.restaurants
    return db, collection

def id_searching():
    restaurant_id = input("Podaj ID restauracji: ")
    db, collection = connection_with_db()
    for document in collection.find({"restaurant_id": restaurant_id}):
        print(document)

def zipcode_searching():
    zipcode = input("Podaj kod pocztowy restauracji: ")
    db, collection = connection_with_db()
    for document in collection.find({"address.zipcode": zipcode}).limit(20):
        print(document)

def name_searching():
    name = input("Podaj nazwę restauracji: ")
    regex_name = re.compile(f"^{name}", re.IGNORECASE)
    db, collection = connection_with_db()
    found_restaurants_number = 0
    for document in collection.find({"name": regex_name}):
        found_restaurants_number += 1
    print(f"\nŁączna liczba restauracji spełniająca kryteria wyszukiwania: {found_restaurants_number}")

    answer = "tak"
    num_skip = 0
    while answer == "tak":
        for document in collection.find({"name": regex_name}).skip(num_skip).limit(num_skip + 20):
            print(document)

        print(f"Wyświetlono restauracje od {num_skip} do {num_skip + 20} z {found_restaurants_number}")
        num_skip += 20
        answer = input("Czy chcesz zobaczyć kolejne 20 restauraji tak/nie?").lower().strip()

def coordinates_searching():
    coorX = float(input("Podaj pierwszą współrzędną: "))
    coorY = float(input("Podaj drugą współrzędną: "))
    dist = float(input("Podaj zakres przeszukiwania: "))

    db, collection = connection_with_db()
    # for document in collection.find({"address": { "$elemMatch": {"coord": {"$gt": -73.0, "$lt": -74.0}} } }, {"address.coord": 1, "name":1}):
    for document in collection.find({"address.coord": {"$lt": coorX + dist, "$gt": coorX - dist} }, {"address.coord": 1, "name":1}):
    # for document in collection.find({"grades.score": {"$gt": 80, "$lt": 100} }, {"grades.score": 1, "name":1}):
        print(document)


def menu_func_2(choose):
    if choose == 1:
        print("Wybrano wyszukiwanie po ID restauracji.")
        id_searching()
    if choose == 2:
        print("Wybrano wyszukiwanie po kodzie pocztowym restauracji")
        zipcode_searching()
    if choose == 3:
        print("Wybrano wyszukiwanie po nazwie restauracji")
        name_searching()
    if choose == 4:
        print("Wyszukiwanie restauracji w twojej okolicy")
        coordinates_searching()
    if choose == 5:
        print("Wyszukiwanie restauracji serwującej daną kuchnię")
    if choose == 6:
        print("Wyszukiwanie restauracji z najwyższą liczbą punktów")



if __name__ == '__main__':

    choose = menu_func()
    menu_func_2(choose)