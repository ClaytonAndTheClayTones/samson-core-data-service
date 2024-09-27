
# Get Started

## Clone the repository

```bash
git clone git@github.com:Datavative/FastApiPrototype.git
```

## Start the database

You will need to have an instance of **Postgres** running on your machine. For added convenience this repo ships with a `docker-compose` file that will set up a Postgres instance for you using authentication credentials that are in the `.env` file. See the `.env-example` file for the required environment variables.

Duplicate the `.env-example` file and rename it to `.env` and update any credentials before proceeding.

```bash
docker-compose up -d
```

## Run the database migrations

### Create a virtual environment for the database migrator service

```bash
cd database

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```
## Run the API service
Open a separate terminal tab and run run the following commands to start the API service.

### Create a virtual environment for the API service

```bash
cd service
python3 -m venv venv
source venv/bin/activate
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Start the service

```bash
python main.py
```
