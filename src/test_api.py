"""Minimal tests for main.py
"""
from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_read_main():
    """This tests if the root endpoint return 200 OK and the right
    message to the user

    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello, World!"}


#def test_stores_name():
 #   """D

  #  """
   # response = client.get("/stores/{specifik}")
    #assert response.status_code == 404
    #assert response.json() == {"detail": "Not Found!"}
