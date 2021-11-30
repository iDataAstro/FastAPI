# CRUD:
```
C: POST : /posts
R: GET  : /posts OR /posts/:id
U: PUT/PATCH : /posts/:id
D: DELETE : /posts/:id
```

## FastAPI AutoDocumentation URL
```text
Swagger UI: http://127.0.0.1:8000/docs
ReDoc UI: http://127.0.0.1:8000/redoc
```

## Docker (for postgressql):

### Pull docker
```bash
docker pull postgres
```

### Run Simple Docker
```bash
docker run --name pg_fastapi -e POSTGRES_PASSWORD=fastapi -d postgres
```

### Run with local directory mapping
```bash
docker run -d \
--name pg_fastapi \
-e POSTGRES_PASSWORD=fastapi \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-v /var/lib/postgresql/data/pgdata:/Users/jatin/docker/pgdata \
-p 5432:5432 \
postgres
```

### To start/stop created container
```bash
docker start pg_fastapi
docker stop pg_fastapi
```

## Using alembic
> Note: For testing purposes we have dropped the tables
1. Install alembic
```bash
pip install alembic
```
2. initialize alembic in "alembic" directory
```bash
alembic init alembid
```
3. Change the alembic/env.py file:
   1. Give access to our sqlalchemy Base object
    ```bash
    from app.models import Base
    ```
   2. Import config to change sqlalchemy.url property    
    ```bash
    from app.config import config as cfg
    ```
   3. Set Database connection
    ```bash
    config.set_main_option('sqlalchemy.url', f"postgresql://{pg_cfg['USERNAME']}:{pg_cfg['PASSWORD']}@{pg_cfg['HOST']}/{pg_cfg['DATABASE']}")
    ```
   4. Target sqlalchemy Base metadata
    ```bash
    target_metadata = Base.metadata
    ```

4. Create/view/apply "revision" manually
   1. Create "revision":
   ```bash
   alembic revision -m "comment for revision"
   ```
   2. Check all "revision":
   ```bash
   alembic heads # Shows all versions
   alembic current # Shows current revision
   ```
   3. Apply "revision"
   ```bash
   # to upgrade head
   alembic upgrade head 
   # to upgrade "5opqlst98g" revision
   alembic upgrade 5opqlst98g
   # to upgrade one step ahead 
   alembic upgrade +1 
   
   # to downgrade one step below
   alembic downgrade -1 
   # to downgrade "5opqlst98g" revision
   alembic downgrade 5opqlst98g 
   ```

5. Create "revision" Auto-generated (using sqlalchemy models)
   ```bash
   alembic revision --autogenerate -m "comment for revision"
   ```

## CORS (Cross Origin Resource Sharing)
* CORS lets you request on web browser on domain to a server on different domain