# Summary

The DICS Core Data Service repository has three major moving parts:

1. The Database Migrator
2. The API itself built primarily as a CRUD service
3. A QDK (Quality Development Kit) implementation that tests all endpoints as modules and provides a development kit for more advanced integration tests.

# Getting Started

## Prerequisites

### Install Pyenv and Python

1. Install pyenv: https://github.com/pyenv/pyenv#installation
2. Run ```pyenv install 3.12.6```
3. Run ```pyenv local 3.12.6```
4. Run ```pyenv global 3.12.6```

### Install Docker Desktop

Install instructions can be found here: https://docs.docker.com/get-started/get-docker/

## Create and initialize the Database

1. Open the /database folder in Visual Studio Code.
2. Make sure your Docker is running.
3. Copy the .env.example file and name it ".env" (these are default values for the database and are fine for local development)
4. Open the terminal and run ```docker compose up```
5. You should see a database instance with the settings from your .env file running in your docker!
6. Connect to your database using PgAdmin4 or similar and the settings prefixed with POSTGRES_ from your .env and run the following:
```
CREATE USER migrator WITH PASSWORD 'mMiIgGrRaAtToOrR1!2@3#4$'; 

GRANT ALL PRIVILEGES ON DATABASE dics TO migrator;

CREATE USER service WITH PASSWORD 'sSeErRvViIcCeE1!2@3#4$';

GRANT 
	SELECT,
	INSERT,
	UPDATE,
	DELETE
ON ALL TABLES IN SCHEMA public TO service;

GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public to service;
```
This is important for setting up the roles that would already exist in a deployed database.

## Migrate the Database

Note: all migration
