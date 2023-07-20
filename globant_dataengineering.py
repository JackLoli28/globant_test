import csv
from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

# PostgreSQL Database Configuration
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'globant'
DB_USER = 'postgres'
DB_PASSWORD = 'jackloli28'

# Function to create the database connection
def create_db_connection():
    connection = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection

# Function to create the tables if they don't exist
def create_tables():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        create_departments_table = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                department VARCHAR(100)
            )
        """
        create_jobs_table = """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                job VARCHAR(100)
            )
        """
        create_employees_table = """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name VARCHAR(100),
                datetime TIMESTAMP,
                department_id INTEGER,
                job_id INTEGER
            )
        """

        cursor.execute(create_departments_table)
        cursor.execute(create_jobs_table)
        cursor.execute(create_employees_table)

        connection.commit()
        cursor.close()
        connection.close()

        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {str(e)}")

# Function to insert data into the database
def insert_data(table_name, data):
    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        placeholders = ', '.join(['%s'] * len(data[0]))
        query = f"INSERT INTO {table_name} VALUES ({placeholders})"

        # Replace empty strings
        data_with_none = [[None if value == '' else value for value in row] for row in data]

        cursor.executemany(query, data_with_none)

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Data inserted into {table_name} successfully.")
    except Exception as e:
        print(f"Error inserting data into {table_name}: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_data():
    try:
        # Process departments.csv
        departments_data = request.files['departments']
        decoded_departments = departments_data.read().decode('utf-8')
        departments_data_list = list(csv.reader(decoded_departments.splitlines()))

        # Process jobs.csv
        jobs_data = request.files['jobs']
        decoded_jobs = jobs_data.read().decode('utf-8')
        jobs_data_list = list(csv.reader(decoded_jobs.splitlines()))

        # Process hired_employees.csv
        hired_employees_data = request.files['hired_employees']
        decoded_hired_employees = hired_employees_data.read().decode('utf-8')
        hired_employees_data_list = list(csv.reader(decoded_hired_employees.splitlines()))

        create_tables()

        insert_data('departments', departments_data_list)
        insert_data('jobs', jobs_data_list)
        insert_data('employees', hired_employees_data_list)

        return jsonify({'message': 'Data uploaded successfully.'})

    except Exception as e:
        return jsonify({'message': f'Error uploading data: {str(e)}'}), 500

@app.route('/metrics/employees-hired-by-quarter', methods=['GET'])
def employees_hired_by_quarter():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT d.department, j.job,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 ELSE NULL END) AS Q1,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 ELSE NULL END) AS Q2,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 ELSE NULL END) AS Q3,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 ELSE NULL END) AS Q4
            FROM departments d
            LEFT JOIN employees e ON d.id = e.department_id
            LEFT JOIN jobs j ON e.job_id = j.id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY d.department, j.job
            ORDER BY d.department, j.job
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        columns = ['department', 'job', 'Q1', 'Q2', 'Q3', 'Q4']
        data = [dict(zip(columns, row)) for row in result]

        return render_template('endpoint1_template.html', data=data)

    except Exception as e:
        return jsonify({'message': f'Error fetching data: {str(e)}'}), 500

@app.route('/metrics/departments-with-most-hired', methods=['GET'])
def departments_with_most_hired():
    try:
        connection = create_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT d.id, d.department, COUNT(e.id) AS hired
            FROM departments d
            LEFT JOIN employees e ON d.id = e.department_id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY d.id, d.department
            HAVING COUNT(e.id) > (SELECT AVG(hired) FROM (SELECT department_id, COUNT(id) AS hired FROM employees WHERE EXTRACT(YEAR FROM datetime) = 2021 GROUP BY department_id) AS t)
            ORDER BY COUNT(e.id) DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        columns = ['id', 'department', 'hired']
        data = [dict(zip(columns, row)) for row in result]

        return render_template('endpoint2_template.html', data=data)

    except Exception as e:
        return jsonify({'message': f'Error fetching data: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(port=4996)
