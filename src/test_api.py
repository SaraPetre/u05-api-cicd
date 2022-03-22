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
    assert response.status_code == 404
    assert response.json() == {"detail": 'Store ArasDjuraffär not found!'}
    shutdown()
def test_stores_in_list():
    '''
    Testen returnera data från listan för att se till att vi får vad vi förväntar oss
    '''
    startup()
    response = client.get("/stores/Djurjouren")
    assert response.status_code == 200
    assert response.json() == {"detail": {"name": "Djuristen", "address": "Upplandsgatan 99, 12345 Stockholm"}}
    shutdown()


def test_sales_exist():
    ''' 
    testen returnera sales ID för att säkerställa att vi får vad vi förväntar oss
    '''
    startup()
    response = client.get("/sales/726ac398-209d-49df-ab6a-682b7af8abfb")
    assert response.status_code == 200
    assert response.json() == {
    "detail": {"store": "Djuristen","timestamp": "2022-01-26T15:24:45","sale_id": "0188146f-5360-408b-a7c5-3414077ceb59",}}
    shutdown()


def test_sales_not_exist():
    ''' 
     Testen returnera felmeddelande om sale id inte existerar
    '''
    startup()
    response = client.get("/sales/0878158f-5360-408b-a7c5-3414077ceb90")
    assert response.status_code == 404
    assert response.json() == {"detail": "this ID does not exist in the list"}
    shutdown()
