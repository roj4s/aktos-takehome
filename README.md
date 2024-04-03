# Aktos take-home technical test

Simple Django API for a generic collection agency to ingest data files provided by their clients.

A demo is deployed at http://aktos.fun:4005.

Go to http://aktos.fun:4005/upload and use the file field in the form to
populate the database from a CSV file.

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

## Running tests

- After the virtual env is created and activated move to same folder
  where pytest.ini and manage.py resides
- Now run pytest as ussual

## Pagination style

- This API uses a Cursor-based pagination style for the consumers and accounts endpoints.
- Also other styles are availble like Page Number that allows moving to an specified page
  and Limit-Offset that allows retrieving a limited ammount of data at an specified offset.
- The Limit-Offset and Page Number approaches are not very efficient in the presence of large
  data sources and in some cases might be unusable.
- On the other hand the Cursor-based approach have fixed-time properties and do not slow down
  as the dataset size increases.
- Also the Cursor-based approach provides a consistent pagination view (i.e the client never sees
  the same item twice when paging through records, even when new items are being inserted by other
  clients during pagination).

#### Limitation of Cursor-based approach

- Moving through pages can only be done forward or backward and not skipped to an specified offset.
- It requires the result set to present a fixed ordering and does not allow the client to arbitrarily
  index into the result set.
- Cursor based pagination requires that there is a unique, unchanging ordering of items in the result
  set. This ordering might typically be a creation timestamp on the records, as this presents a consistent
  ordering to paginate against.
