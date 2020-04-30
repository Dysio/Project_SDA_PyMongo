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
        raise ValueError

    return choose

if __name__ == '__main__':

    print('''Menu:
1. Wyszukiwanie restauracji po ID
2. Wyszukiwanie restauracji po kodzie pocztowym
3. Wyszukiwanie restauracji po nazwie
4. Wyszukiwanie restauracji w twojej okolicy
5. Wyszukiwanie restauracji serwującej zadaną kuchnię
6. Wyszukiwanie restauracji w obrębie dzielnicy, TOP X''')

    menu_func()