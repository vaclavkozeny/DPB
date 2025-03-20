import redis
from collections import Counter
import time
import re
import matplotlib.pyplot as plt
r = redis.Redis(host='localhost', port=6379, db=0,decode_responses=True)


MyPath = "/home/vaclav/Stažené/data.txt"
slovaKey = "struct:slova"
pismenaKey = "struct:pismena"

def text_analysis(path):
    pismena = Counter()
    slova = Counter()
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.lower()
            pismena.update(znak for znak in line if znak.decode('utf-8').isalpha()) 
            cista_slova = re.findall(r'\b\w+\b', line)
            slova.update(cista_slova)
    save_structure(pismena, pismenaKey,None)
    save_structure(slova,slovaKey,None)
    return pismena, slova


def get_words(N,M,slova):
    filtered = {word: count for word, count in slova.items() if len(word) >= M}
    return Counter(filtered).most_common(N)
        

def save_structure(structure, key, ttl):
    r.zadd(key,structure)
    r.ttl(key,ttl)

def load_structure(key):
    raw_data = r.zrange(key, 0, -1, withscores=True)
    retrieved_dict = {key: int(value) for key, value in raw_data}
    return retrieved_dict

def use_cache():
    if(r.exists(pismenaKey) == False or r.exists(slovaKey) == False ):
        text_analysis(MyPath)
    else:
        return load_structure(pismenaKey), load_structure(slovaKey)

def analyze_czech(pismena, slova):
    filtrovana_pismena = {k: v for k, v in pismena.items() if re.match(r'^[a-záčďéěíňóřšťúůýž]$', k)} #filtr na česká písmena
    suma = sum(filtrovana_pismena.values()) # suma hodnot
    #vypis
    for pismeno, pocet in reversed(filtrovana_pismena.items()):
        print(f'{pismeno}: {pocet}, {(pocet / suma) * 100}%')
    #graf
    filtrovana_pismena = dict(sorted(filtrovana_pismena.items(),key = lambda x: x[1], reverse=True))
    normalizovane_hodnoty = [hodnota / suma for hodnota in filtrovana_pismena.values()] #prevod na procenta
    plt.bar(filtrovana_pismena.keys(),normalizovane_hodnoty)
    plt.savefig('graf.png')
    #nejcastejsi slovo
    print('nejcastejsi slovo:')
    print(get_words(1,1,slova))
    #10 slov o delce 8+
    print('nejcastejsi slova s delkou 8+')
    print(get_words(10,8,slova))
    print('pocet slov o delce 10+')
    print(len(get_words(None,10,slova)))

def search(slovo):
    pocet_vyskytu = r.zscore(slovaKey, slovo)

    if pocet_vyskytu is not None:
        print(f'Slovo "{slovo}" má {int(pocet_vyskytu)} výskytů.')
    else:
        print(f'Slovo "{slovo}" nebylo nalezeno v řazené sadě.')

start = time.time()
pismena, slova = use_cache()
analyze_czech(pismena, slova)
print(r.zrevrange(pismenaKey,0,4,withscores=1))
print(r.zrange(pismenaKey,0,4,withscores=1))
print(r.zrevrange(slovaKey,0,9,withscores=1))
search("ještěd")
end = time.time()
cas = end - start
print(cas)