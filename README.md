# CRUD:
```
C: POST : /posts
R: GET  : /posts OR /posts/:id
U: PUT/PATCH : /posts/:id
D: DELETE : /posts/:id
```

## FastAPI AutoDocumentation URL
```
Swagger UI: http://127.0.0.1:8000/docs
ReDoc UI: http://127.0.0.1:8000/redoc
```

## Docker (for postgressql):

### Pull docker
```
docker pull postgres
```

### Run Simple Docker
```
docker run --name pg_fastapi -e POSTGRES_PASSWORD=fastapi -d postgres
```

### Run with local directory mapping
```
docker run -d \
--name pg_fastapi \
-e POSTGRES_PASSWORD=fastapi \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v /var/lib/postgresql/data/pgdata:/Users/jatin/docker/pgdata \
-p 5432:5432 \
postgres
```

### To start/stop created container
```
docker start pg_fastapi
docker stop pg_fastapi
```