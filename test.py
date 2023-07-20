import requests

# Replace with the appropriate URL of your API
base_url = "http://localhost:5000"

def import_data(file_path, endpoint):
    url = f"{base_url}/{endpoint}"
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, files=files)
    return response.json()

if __name__ == "__main__":
    # Replace with the paths to your CSV files
    departments_file = "path/to/departments.csv"
    jobs_file = "path/to/jobs.csv"
    hired_employees_file = "path/to/hired_employees.csv"

    # Import data using API endpoint '/import_data'
    import_data_response_1 = import_data(departments_file, "import_data")
    import_data_response_2 = import_data(jobs_file, "import_data")
    import_data_response_3 = import_data(hired_employees_file, "import_data")

    print("Import Data Responses:")
    print("Departments:", import_data_response_1)
    print("Jobs:", import_data_response_2)
    print("Hired Employees:", import_data_response_3)

    # Test the '/explore_data' endpoint (optional)
    response = requests.get(f"{base_url}/explore_data")
    print("\nExplore Data Response:")
    print(response.json())
