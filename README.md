# Task API

This project is a Django-based REST API for managing attributes, products, catalogs, and related entities. The API is built with Django Rest Framework (DRF) and provides endpoints for importing data, listing models, and viewing details of specific records.

## Features

- **Import Data**: Import multiple records for different models in a single request.
- **List Models**: Retrieve a list of all records for a specified model.
- **Detail View**: View detailed information about a specific record by its ID.

## Endpoints

## 1. Import Data

- **URL**: `/import`
- **Method**: `POST`
- **Description**: Allows importing data for different models. The input should be a list of JSON objects where each object contains a model name as the key and the corresponding fields as the value.
- **Note**: If you import value with id, that already exists in database, the old value will be overridden

- **Example Input**:
  ```json
  [
      {
          "AttributeName": {
              "name": "Color"
          }
      },
      {
          "Product": {
              "name": "T-Shirt",
              "price": 19.99
          }
      }
  ]

### Response:
- **201 Created** if data is successfully imported.
- **400 Bad Request** if there's an issue with the input data.

## 2. List Models

- **URL**: `/detail/<str:model_name>`
- **Method**: GET
- **Description**: Returns a list of all records for the specified model.

### Response:
- **200 OK** with a list of records.
- **400 Bad Request** if the model name is invalid.

## 3. Detail View

- **URL**: `/detail/<str:model_name>/<int:id>/`
- **Method**: GET
- **Description**: Returns detailed information about a specific record by its ID.
- **Note**: Names and values with reference to another object are replaced by the object name and object detail.

### Response:
- **200 OK** with the record's details.
- **400 Bad Request** if the record is not found.

## Usage

### Prerequisites

#### Install PostgreSQL:
- Download and install PostgreSQL from the official website: [PostgreSQL Download](https://www.postgresql.org/download/).
- During installation, set up a PostgreSQL user (e.g., `taskuser`) and a password.

#### Create Database:
- After installing PostgreSQL, create a new database for the project.
- You can do this via the command line or using a PostgreSQL client like pgAdmin.
- Example command to create a database:
  ```bash
  psql -U taskuser -c "CREATE DATABASE taskdb;"
  ```

### Installation and Setup


#### Install requirements
  ```
  pip install -r requirements.txt
  ```

#### Configure Database:
- create .env file with secrets
- Example configuration:
```
DEBUG=1
SECRET_KEY=default-secret

DB_NAME=task_api
DB_USER=admin
DB_PASSWORD=password
DB_HOST=127.0.0.1
DB_PORT=5432
```

#### Run migrations
```
python3 manage.py migrate
```

#### Run migrations
```
python manage.py runserver
```


