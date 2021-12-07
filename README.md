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
* Add following code to main.py file just after `app = FastAPI()`
```python
# "*" - Means all domains allowed.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## FastAPI Demo Application
[FastAPI Demo Application](https://fastapi-idataastro.herokuapp.com/docs)


## Deploy Application on server (EC2)
1. Create your server using ubuntu os
2. Update linux 
```bash
sudo apt-get update && sudo apt-get upgrade
```
3. Install PostgreSQL on server
```bash
sudo apg-get install postgresql postgresql-contrib
```
   * Update password for "postgres" user in psql
   ```bash
   \password postgres
   ```
   * Disable 'peer' authentication to work on localbox
     * Update pg_hbg.conf 
       * change "peer" to "md5" (for local postgres user)
   * To access the database from pgadmin
     * Update pg_server.conf
4. Create user to deploy application
```bash
useradd jatin
```
5. Set Environment variables for application
   * Create .env_vars file and add all variables init
   * Add following command to /home/jatin/.profile file
   ```bash
   set -o allexport; source /home/jatin/.env_vars; set +o allexport;
   ```
   * To check environment variables
   ```bash
   printenv
   ```
6. Clone repository into your home directory
```bash
cd /home/jatin
mkdir app
cd app
git clone <GIT-URL> . # PUT DOT TO CREATE IN CURRENT DIRECTORY
```
7. Install miniconda or virtualenv to create environment and install dependencies
```bash
conda create --prefix .venv python=3.7 -y
conda activate .venv
pip install -r requirements.txt
```
8. To apply alembic upgrade (To create tables in database)
```bash
cd /home/jatin/app
conda activate .venv
alembic upgrade head
```
9. To use multi-process our app
```bash
# Install required packages
pip install gunicorn httptools uviloop
# To start manually on terminal
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```
10. To setup our app as service named: fastapi-app.service
    1. create file "fastapi-app.service" in /etc/systemd/system
    2. copy fastapi.service file into above file
    3. To start / stop / status : 
    ```bash
    systemctl start / stop / status fastapi-app
    ```
    5. To start our service on reboot
    ```bash
    systemctl enable fastapi-app
    ```
11. Setup NGINX as proxy webserver for our application
```bash
# Install nginx
sudo apt-get install nginx -y
# Start nginx service
systemctl start nginx
# Configure nginx
cd /etc/nginx/sites-available
vi default
# Add "location" block as mentioned in nginx file
# and restart service
systemctl restart nginx
```
12. Setup firewall on server
    * We can use built-in firewall called "ufw"
    * Check status of ufw firewall
    ```bash
    sudo ufw status
    ```
    * Setup rules for ufw
    ```bash
    sudo ufw allow http 
    sudo ufw allow https
    sudo ufw allow ssh
    sudo ufw allow 5432 # allow postgres outside server - using pgadmin
    ```
    * Start firewall
    ```bash
    sudo ufw enable
    ```
    * To delete any rule 
    ```bash
    sudo ufw delete allow 5432
    ```
## Dockerize application
* Create a docker file with following code
```bash
# specify python version
FROM python:3.9.7

# specify working directory
WORKDIR /usr/src/app

# copy requirements.txt file to working directory
COPY requirements.txt ./

# install dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# copy source files to working directory
COPY . .

# start app with following command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
```

* Build docker image using the following command
```bash
# -t: tag name for image
# .: specify Dockerfile path
docker build -t fastapi . 

# to check image
docker image ls
```

* Using docker compose to build and start containers which we build using Dockerfile
    * Create docker-compose-dev.yaml file with following lines:
      * version: docker-compose version
      * services: specify the services to run on docker
      * api: service to run
        * build: build docker image from directory
        * ports: specify the ports to map docker to localhost
        * volumes: sync local code changes to docker image
        * env_file: specify the environment variables file
        * environment: specify the environment variables
        * command: specify the command to run service
        * depends_on: specify the dependencies of service (here on postgres)
      * postgres: another service - postgres db
        * image: name of docker image to pull from server
        * expose: to connect on localhost only (app to db)
        * ports: to connect on localhost and from outside world as well
        * environment: specify the environment variables
        * volumes: specify the volume to persist data on restart
      * volumes: separate service which can be accessed by other docker-compose
        * postgres-db: postgres db volume
```yaml
version: "3"
    services:
        api:
            build: .
            ports:
                - 8000:8000
            volumes:
                - ./:/usr/src/app
            # env_file:
            #     - ./.env
            environment:
                - DATABASE_HOSTNAME=postgres # postgres match to postgres service name
                - DATABASE_PORT=5432
                - DATABASE_PASSWORD=password123
                - DATABASE_NAME=fastapi
                - DATABASE_USERNAME=postgres
                - SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
                - ALGORITHM=HS256
                - ACCESS_TOKEN_EXPIRE_MINUTES=30
            command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
            depends_on:
                - postgres # specify this in environment variable DATABASE_HOSTNAME
                
        postgres:
            image: postgres
            expose:
              - 5432
            #ports:
            # - 5432:5432
            environment:
                - POSTGRES_PASSWORD=password123
                - POSTGRES_DB=fastapi
            volumes:
                - postgres-db:/var/lib/postgresql/data

volumes:
  postgres-db:
```

    * To start/stop docker-compose
```bash
# to start docker-compose
docker compose up -d 

# to start with compose file name
docker compose -f docker-compose.yaml up -d

# to rebuild images
docker compose up -d --build

# to stop docker-compose
docker compose down
# to stop with file name
docker compose -f docker-compose.yaml down
```

    * To check logs of docker-compose 
```bash
docker logs fastapi_api_1 #image name
```
    * To interact with docker images
```bash
docker exec -it fastapi_api_1 bash
```