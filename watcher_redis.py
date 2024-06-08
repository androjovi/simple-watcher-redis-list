import redis
import os
import multiprocessing
import time
import requests
from datetime import datetime

r = redis.Redis(host="localhost", port=6379)
r_key = "myKey"
num_process = 2

def watching_key(index):
    i = 1
    # start forever looping
    while True:
        # watching key "test" in redis, brpop block if nothing data sent to key
        mq = r.brpop(f"{r_key}", 0)
        # check value
        if mq is not None:
            try:
                # unpacking array
                k, v = mq
                # decode value because its bytes
                v = v.decode('utf-8')
                # time.sleep(int(v))
                worker_function(index, v, os.getpid())

            except ValueError as e:
                print(e)

def worker_function(index, v, pid):
    start_time = datetime.now()
    url = 'https://cetakan.wahana.com'
    response = requests.post(url)
    end_time = datetime.now()
    print(response.text, index, v, pid, format(end_time - start_time))

def repush_key(v):
    r.lpush(f"{r_key}", v)

if __name__ == '__main__':
    with multiprocessing.Pool(processes=num_process) as pool:
        pool.map(watching_key, range(num_process))
        # make it async
        res = pool.apply_async(watching_key, range(num_process))
        print(res.get(timeout=1))