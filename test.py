import pytest
import requests
import psycopg2
from flask import Flask
from globant_dataengineering import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_upload_data(client):
    response = client.post("/upload")
    assert response.status_code == 200
    assert b"Data uploaded successfully." in response.data

def test_employees_hired_by_quarter(client):
    response = client.get("/metrics/employees-hired-by-quarter")
    assert response.status_code == 200
    assert b"Q1" in response.data
    assert b"Q2" in response.data
    assert b"Q3" in response.data
    assert b"Q4" in response.data

def test_departments_with_most_hired(client):
    response = client.get("/metrics/departments-with-most-hired")
    assert response.status_code == 200
    assert b"id" in response.data
    assert b"department" in response.data
    assert b"hired" in response.data
