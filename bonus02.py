import redis
r = redis.Redis(host='localhost', port=6379, db=0,decode_responses=True)

r.zadd('set:games_py',{'Alfréd':888,'Čéňa':999,'Pepa':111, 'Marek':222, 'Tomáš':333, 'Michal':444, 'Hynek':555, 'Lucifer':666, 'Zikmund':777, 'Karel':889, 'Václav':2, 'Jan':1})
print(f"tri nejlepsi skore: {r.zrevrange('set:games_py',0,2, withscores=1)}")
print(f"nejhorsi skore: {r.zrange('set:games_py',0,0,withscores=1)}")
print(f"pocet hracu pod 100 skore: {r.zcount('set:games_py',0,100)}")
print(f"hraci s vice nez 850 body: {r.zrevrangebyscore('set:games_py',1000,850,withscores=1)}")
print(f"alfredova pozice: {r.zrevrank('set:games_py','Alfréd')+1}")
r.zincrby('set:games_py',12,'Alfréd')
print(f"alfredova nova pozice: {r.zrevrank('set:games_py','Alfréd')+1}")
