from pymongo import MongoClient
from pprint import pprint

# tworzenie połączenia
client = MongoClient()

# wybór bazy danych
db = client.test

collection = db.restaurants

# wyswietli pierwsza wartosc
# print(collection.find_one())

# for document in collection.find({"borough": "Bronx"}).limit(3):
#     print(document)

for document in collection.find({'borough': 'Bronx'}, {'name': 1, '_id': 0}).limit(3):
    print(document)

