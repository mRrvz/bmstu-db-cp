```bash
curl -X POST -H "Content-Type: application/json" https://localhost/api/v1/user/registration -d '{ "username": "admin", "password": "mysupersecretpassword", "email": "email", "status": "bruh" }' -k

curl -X POST -H "Content-Type: application/json" https://localhost/api/v1/user/login -d '{ "username": "admin" }' -k

export TOKEN=<access_token>

curl -X GET https://localhost/api/v1/user/info -H 'Accept: application/json' -H "Authorization: Bearer ${TOKEN}" -k
```
