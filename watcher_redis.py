import redis

r = redis.Redis(host="localhost", port=6379)

i = 1
# start forever looping
while True:
    # watching key "test" in redis, brpop block if nothing data sent to key
    mq = r.brpop("myKey", 0)
    # check value
    if mq is not None:
        try:
            # unpacking array
            k, v = mq
            # decode value because its bytes
            v = v.decode('utf-8')
            print(v)
        except ValueError as e:
            print(e)