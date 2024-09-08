## Airflow

### Dependencies
- python `brew install python@3.10`
- install docker and docker compose

### Run docker compose
```shell
mkdir logs
mkdir plugins

docker compose up airflow-init 
docker-compose up -d
```

### Dev
- install python dependencies
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```