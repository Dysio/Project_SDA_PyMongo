from pymongo import MongoClient

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


def menu_func_2(choose):
    if choose == 1:
        print("Podaj ID restauracji: ")
    if choose == 2:
        print("Podaj kod pocztowy restauracji")
    if choose == 3:
        print("Podaj nazwę restauracji")
    if choose == 4:
        print("Wyszukiwanie restauracji w twojej okolicy")
    if choose == 5:
        print("Wyszukiwanie restauracji serwującej daną kuchnię")
    if choose == 6:
        print("Wyszukiwanie restauracji z najwyższą liczbą punktów")


if __name__ == '__main__':

    choose = menu_func()
    menu_func_2(choose)