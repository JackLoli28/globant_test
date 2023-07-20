# Globant Data Engineering Test

Author: Jack Loli

This repository contains the code for a local REST API that handles data migration and provides specific metrics related to departments, jobs, and employees.
The API is built using Flask and connects to a PostgreSQL database to store the data.

## Section 1: API

In the context of a DB migration with three different tables (departments, jobs, employees), the API provides the following functionalities:

1. Receive historical data from CSV files and upload them to the new database.
2. Insert batch transactions (1 up to 1000 rows) with one request.

### API Endpoints

- `POST /upload`: Uploads CSV files (departments.csv, jobs.csv, and hired_employees.csv) to populate the database.
- `GET /metrics/employees-hired-by-quarter`: Provides the number of employees hired for each job and department in 2021 divided by quarter.
- `GET /metrics/departments-with-most-hired`: Lists the IDs, names, and number of employees hired for each department that hired more employees than the mean of employees hired in 2021 for all departments.

## Section 2: SQL Metrics

The API provides two endpoints to fetch specific metrics from the database related to employee hiring. The results are displayed using HTML templates.

### Requirements

1. Number of employees hired for each job and department in 2021 divided by quarter.
2. List of IDs, names, and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all departments, ordered by the number of employees hired (descending).

## Installation and Usage

1. Clone the repository:

git clone https://github.com/JackLoli28/globant_test.git

2. Install the required Python packages:

pip install -r requirements.txt

3. Update the PostgreSQL database configuration (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD) in the `globant_dataengineering.py` file.

4. Run the API:

python globant_dataengineering.py

5. Use `curl` to interact with the endpoints.Make sure to replace the file names with the actual names of your CSV files and execute the command in the same directory where the CSV files are located.

curl -X POST -F "departments=@departments.csv" -F "jobs=@jobs.csv" -F "hired_employees=@hired_employees.csv" http://localhost:4996/upload

## Automated Tests

The API includes automated tests to ensure the correctness of its functionalities. The tests are implemented using `pytest`. To run the tests, use the following command:

pytest test.py

