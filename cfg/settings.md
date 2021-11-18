# Настройка PostgreSQL

```bash
apt install postgresql-contrib postgresql-plpython3-11
su - postgres
psql
```

```
\c 
\i /cfg/init_postgres.sql
```

# Настройка Tarantool

Добавить в ``docker-compose command``: ``tarantool /cfg/init_tarantool.lua``


# Проверка http2, http3

* http2: `nghttp -ans https://localhost/index.html`
* http3: `curl -IL https://nginx --http3` (в контейнере)
