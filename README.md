# Aktos take-home technical test

Simple Django API for a generic collection agency to ingest data files provided by their clients.

## How to run

#### Using docker-compose

- Make sure you have docker-compose installed
- In your shell make sure your are positioned at same
  folder as the docker-compose.yaml file
- Run docker-compose up --build
- If everything went ok the app should be accessible
  at http://localhost:4005 and the database at localhost:5432

#### Using custom env:

- Create an environment using conda or pyenv.
- Use environment.yaml or requirements.txt to install depedencies
- Activate the environment
- Run migrations python manage.py migrate
- Run server python manage.py runserver
