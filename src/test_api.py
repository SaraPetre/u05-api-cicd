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


def test_stores():
    '''
    Testen returnera 200
    '''
    startup()    
    response = client.get("/stores")
    assert response.status_code == 200
    assert response.json() == {"data": [{"name": "Djurjouren", "address": "Upplandsgatan 99, 12345 Stockholm"},
    {"name": "Djuristen","address": "Skånegatan 420, 54321 Falun"},
    {"name": "Den Lilla Djurbutiken","address": "Nätverksgatan 22, 55555 Hudiksvall"},
    {"name": "Den Stora Djurbutiken","address": "Routergatan 443, 54545 Hudiksvall"},
    {"name": "Noahs Djur & Båtaffär","address": "Stallmansgatan 666, 96427 Gävle"}]
}
    shutdown()



def test_city():
    '''
    Testen returnera data från listan för att se till att vi får vad vi förväntar oss
    '''
    startup()
    response = client.get("/city?zip=12345")
    assert response.status_code == 200
    assert response.json() == {"data": ["Stockholm"]}
    shutdown()

def test_city_non_existing():
    '''
    Testen returnera data 404
    '''
    startup()
    response = client.get("/city/99999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
    shutdown()
