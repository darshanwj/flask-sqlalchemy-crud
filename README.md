# flask-sqlalchemy-crud

## create a user
```
$ curl -X POST http://localhost:8081/user -d '{"name":"works?"}' -H "Content-type: application/json"
```

## update a user
```
$ curl -X PUT http://localhost:8081/user/1 -d '{"name":"with commits"}' -H "Content-type: application/json"
```

## get all users
```
$ curl http://localhost:8081/
```

## get single user
```
$ curl http://localhost:8081/user/1
```