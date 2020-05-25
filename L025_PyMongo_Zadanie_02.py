from pymongo import MongoClient
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

    choose = input('Wybierz interesującą Cie opcję: ')
    # try:
    #     choose = int(input('Wybierz interesującą Cie opcję: '))
    # except ValueError:
    #     raise ValueError('Podana wartość musi być cyfrą!')
    if choose not in ('1','2','3','4','5','6'):
        raise ValueError('Podana wartość musi być cyfrą od 1 do 6!')

    return choose

def connection_with_db():
    client = MongoClient()
    db = client.test
    collection = db.restaurants
    return db, collection

def answer_func():
    answer = input("Czy chcesz zobaczyć kolejne 20 restauraji tak/nie?").lower().strip()
    while answer not in ('tak', 'nie'):
        answer = input("Czy chcesz zobaczyć kolejne 20 restauraji tak/nie?").lower().strip()
    return answer

def id_searching(collection):
    restaurant_id = input("Podaj ID restauracji: ")
    for document in collection.find({"restaurant_id": restaurant_id}):
        print(document)

def zipcode_searching(collection):
    zipcode = input("Podaj kod pocztowy restauracji: ")
    for document in collection.find({"address.zipcode": zipcode}).limit(20):
        pprint(document)

def name_searching(collection):
    name = input("Podaj nazwę restauracji: ")
    # regex_name = re.compile(f"(^|.){name}", re.IGNORECASE)

    # found_restaurants_number = collection.count_documents({"name": regex_name})
    found_restaurants_number = collection.count_documents({'name': {'$regex':f'(^|.){name}', '$options':'-i'}})
    print(f"\nŁączna liczba restauracji spełniająca kryteria wyszukiwania: {found_restaurants_number}")

    answer = "tak"
    num_skip = 0
    while answer == "tak":
        # for document in collection.find({"name": regex_name}).skip(num_skip).limit(num_skip + 20):
        for document in collection.find({"name": {"$regex": f"(^|.){name}", "$options":"-i"}}).skip(num_skip).limit(num_skip + 20):
            print(document)

        print(f"Wyświetlono restauracje od {num_skip} do {num_skip + 20} z {found_restaurants_number}")
        num_skip += 20
        if num_skip > found_restaurants_number:
            print("Brak więcej wyników do wyświetlenia.")
            break

        answer = answer_func()

def coordinates_searching(collection):
    coorX = float(input("Podaj pierwszą współrzędną: "))
    coorY = float(input("Podaj drugą współrzędną: "))
    dist = float(input("Podaj zakres przeszukiwania: "))

    found_restaurants_number = collection.count_documents({"address.coord.0": {"$gt": (coorX - dist), "$lt": (coorX + dist)},
                                     "address.coord.1": {"$gt": (coorY - dist), "$lt": (coorY + dist)}})

    answer = "tak"
    num_skip = 0
    while answer == "tak":
        for document in collection.find({"address.coord.0": {"$gt": (coorX - dist), "$lt": (coorX + dist)},
                                         "address.coord.1": {"$gt": (coorY - dist), "$lt": (coorY + dist)}  },
                                        ).skip(num_skip).limit(num_skip + 20):
            print(document)
        print(f"Wyświetlono restauracje od {num_skip} do {num_skip + 20} z {found_restaurants_number}")
        num_skip += 20
        if num_skip > found_restaurants_number:
            print("Brak więcej wyników do wyświetlenia.")
            break

        answer = answer_func()

def kitchen_borough_searching(collection):
    cuisine = input("Podaj kuchnie: ").capitalize()
    if cuisine == "American":
        cuisine = cuisine + " "

    condition_borough = input("Czy chcesz podać dzielnice? tak/nie: ")
    if condition_borough == "tak":
        borough = input("Podaj dzielnicę: ").capitalize()

    answer = "tak"
    num_skip = 0
    if condition_borough == "tak":

        found_restaurants_number = collection.count_documents({"cuisine": cuisine, "borough": borough})

        while answer == "tak":
            for document in collection.find({"cuisine": cuisine, "borough":borough}).skip(num_skip).limit(num_skip + 20):
                print(document)
            print(f"Wyświetlono restauracjie od {num_skip} do {num_skip + 20} z {found_restaurants_number}")
            num_skip += 20
            if num_skip > found_restaurants_number:
                print("Brak więcej wyników do wyświetlenia.")
                break
            answer = answer_func()
    else:

        found_restaurants_number = collection.count_documents({"cuisine": cuisine})

        while answer == "tak":
            for document in collection.find({"cuisine": cuisine}).skip(num_skip).limit(num_skip + 20):
                print(document)
            print(f"Wyświetlono restauracjie od {num_skip} do {num_skip + 20} z {found_restaurants_number}")
            num_skip += 20
            if num_skip > found_restaurants_number:
                print("Brak więcej wyników do wyświetlenia.")
                break
            answer = answer_func()


def borough_searching(collection):
    borough = input("Podaj dzielnicę: ")
    numberX = int(input("Podaj ile najlepszych restauracji chcesz zobaczyć: "))

    for document in collection.find({"borough": borough}).sort([("grades.score", -1)]).limit(numberX):
        print(document)


def menu_func_2(choose):
    client = MongoClient()
    db = client.test
    collection = db.restaurants

    if choose == '1':
        print("Wybrano wyszukiwanie po ID restauracji.")
        id_searching(collection)
    if choose == '2':
        print("Wybrano wyszukiwanie po kodzie pocztowym restauracji")
        zipcode_searching(collection)
    if choose == '3':
        print("Wybrano wyszukiwanie po nazwie restauracji")
        name_searching(collection)
    if choose == '4':
        print("Wyszukiwanie restauracji w twojej okolicy")
        coordinates_searching(collection)
    if choose == '5':
        print("Wyszukiwanie restauracji serwującej daną kuchnię")
        kitchen_borough_searching(collection)
    if choose == '6':
        print("Wyszukiwanie restauracji z najwyższą liczbą punktów")
        borough_searching(collection)





if __name__ == '__main__':

    choose = menu_func()
    menu_func_2(choose)