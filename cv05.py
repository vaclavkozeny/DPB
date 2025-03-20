from init import collection
from pprint import pprint
import datetime

print(collection.find_one())

'''
DPB - 5. Cvičení

Implementujte jednotlivé body pomocí PyMongo knihovny - rozhraní je téměř stejné jako v Mongo shellu.
Před testováním Vašich řešení si nezapomeňte zapnout Mongo v Dockeru.

Pro pomoc je možné např. použít https://www.w3schools.com/python/python_mongodb_getstarted.asp

Funkce find vrací kurzor - pro vypsání výsledku je potřeba pomocí foru iterovat nad kurzorem:

cursor = collection.find(...)
for restaurant in cursor:
    print(restaurant) # případně print(restaurant['name'])

Všechny výsledky limitujte na 10 záznamů. Nepoužívejte české názvy proměnných!
'''


def print_delimiter(n):
    print('\n', '#' * 10, 'Úloha', n, '#' * 10, '\n')

# 1. Vypsání všech restaurací 
print_delimiter(1)
cursor = collection.find()
for res in cursor.limit(5):    
    pprint(res)
# 2. Vypsání všech restaurací - pouze názvů, abecedně seřazených
print_delimiter(2)
cursor = collection.find({},{"name":1}).sort({"name":1})
for res in cursor.limit(10):    
    pprint(res['name'])
# 3. Vypsání pouze 5 záznamů z předchozího dotazu
print_delimiter(3)
cursor = collection.find({},{"name":1}).sort({"name":1})
for res in cursor.limit(5):    
    pprint(res['name'])
# 4. Zobrazte dalších 10 záznamů
print_delimiter(4)
cursor = collection.find({},{"name":1}).sort({"name":1}).limit(10).skip(10)
for res in cursor:    
    pprint(res['name'])
# 5. #Vypsání restaurací ve čtvrti Bronx (čtvrť = borough)
print_delimiter(5)
cursor = collection.find({'borough':'Bronx'})
for res in cursor.limit(5):    
    pprint(res)
# 6. Vypsání restaurací, jejichž název začíná na písmeno M
print_delimiter(6)
cursor = collection.find({'name':{"$regex":"^M"}})
for res in cursor.limit(5):    
    pprint(res['name'])
# 7. Vypsání restaurací, které mají skóre větší než 80
print_delimiter(7)
cursor = collection.find({"grades.score":{"$gt": 80}})
for res in cursor.limit(5):    
    pprint(res['name'])
# 8. Vypsání restaurací, které mají skóre mezi 80 a 90
print_delimiter(8)
cursor = collection.find({ "grades": { "$elemMatch": { "score": { "$gt": 80, "$lt": 90 } } } })
for res in cursor.limit(5):    
    pprint(res['name'])
'''
Bonusové úlohy:
'''

# 9. Vypsání všech restaurací, které mají skóre mezi 80 a 90 a zároveň nevaří americkou (American) kuchyni
print_delimiter(9)
cursor = collection.find({ "grades": { "$elemMatch": { "score": { "$gt": 80, "$lt": 90 } } }, "cuisine":{"$ne":"American"}})
for res in cursor:    
    pprint(res['name'])
# 10. Vypsání všech restaurací, které mají alespoň osm hodnocení
print_delimiter(10)
cursor = collection.find({"$expr": {"$gte": [{ "$size": "$grades" }, 8]}})
for res in cursor.limit(10):    
    pprint(res['name'])
# 11. Vypsání všech restaurací, které mají alespoň jedno hodnocení z roku 2014 
print_delimiter(11)
cursor = collection.find({"grades": {"$elemMatch": {"date": {"$gte": datetime.datetime(2014, 1, 1),"$lt": datetime.datetime(2015, 1, 1)}}}})
for res in cursor.limit(10):    
    pprint(res['name'])
'''
V této části budete opět vytvářet vlastní restauraci.

Řešení:
Vytvořte si vaši restauraci pomocí slovníku a poté ji vložte do DB.
restaurant = {
    ...
}
'''

# 12. Uložte novou restauraci (stačí vyplnit název a adresu)
print_delimiter(12)
collection.insert_one({"name":'nova restaurace',"address": {"building": '123',"street": 'Prazska',"zipcode": '46001'},"cuisine":'asian'})
# 13. Vypište svoji restauraci
print_delimiter(13)
cursor = collection.find({"name":"nova restaurace"})
for res in cursor.limit(10):    
    pprint(res)
# 14. Aktualizujte svoji restauraci - změňte libovolně název
print_delimiter(14)
collection.update_one({"name": 'nova restaurace'},{"$set":{"name":'super restaurace'}})
# 15. Smažte svoji restauraci
# 15.1 pomocí id (delete_one)
id = collection.find_one({"name":"super restaurace"},{"_id":1})
print(id)
collection.delete_one(id)
# 15.2 pomocí prvního nebo druhého názvu (delete_many, využití or)
collection.delete_many({"$or":[{"name":"nova restaurace"},{"name":"super restaurace"}]})
print_delimiter(15)


'''
Poslední částí tohoto cvičení je vytvoření jednoduchého indexu.

Použijte např. 3. úlohu s vyhledáváním čtvrtě Bronx. První použijte Váš již vytvořený dotaz a na výsledek použijte:

cursor.explain()['executionStats'] - výsledek si vypište na výstup a všimněte si položky 'totalDocsExamined'

Poté vytvořte index na 'borough', zopakujte dotaz a porovnejte hodnoty 'totalDocsExamined'.

S řešením pomůže https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.create_index
'''
print_delimiter(11)
