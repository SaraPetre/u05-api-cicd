"""Minimal tests for api.py
"""

from fastapi.testclient import TestClient

import psycopg

from api import app  # ,DBMock

client = TestClient(app)


def test_read_main():
    """This tests if the root endpoint return 200 OK and the right
    message to the user

    """
    startup()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello, World!"}
    shutdown()


def startup():
    "D"

    app.db = psycopg.connect(
        """dbname=u05 user=postgres host=doe21-db.grinton.dev
         password=DjExUSMcwWpzXziT port=5432
        """)


def shutdown():
    "D"

    app.db.close()


def test_specific_store_not_in_list():
    '''
    Testen returnera data (namn och fullständig address) för en specifik
    butik, vald via namn om ett namn som inte finns i DB anges,
    returnera 404 Not Found
    '''
    startup()
    # app.db = DBMock()
    response = client.get("/stores/ArasDjuraffär")
    # assert response.status_code == 200
    # assert response.json() == [[1, "a", "b"]]
    assert response.status_code == 404
    assert response.json() == {'detail': 'Store ArasDjuraffär not found!'}
    shutdown()
