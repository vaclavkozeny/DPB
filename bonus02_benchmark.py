import redis
import time
r = redis.Redis(host='localhost', port=6379, db=0,decode_responses=True)

data = {}
start = time.time()
for i in range(1000000):
    data[f"benchmark:{i}"] = i
r.mset(data)
r.flushall()
end = time.time()
cas = end - start
print(cas)