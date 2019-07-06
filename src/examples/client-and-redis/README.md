# Client and Redis Server

This example contains a simple client that pings a Redis server:

```sh
echo PING | nc -v redis 6379
```

Note that the client assumes a Redis instance is running at `redis:6379` - `dockerized` will take care of that! Just run:

```sh
$ dockerized exec ./client
Starting dockerized_redis_1 ... done
Pinging the Redis service...
redis (172.20.0.2:6379) open
+PONG
```

# What happened?

`dockerized` simply ran `docker-compose` to spin up two containers: a Redis container listening on `redis:6379` and another container to run the command (`./client`) in. It then executed the command in that container.
