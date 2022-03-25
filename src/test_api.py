"""Minimal tests for api.py
"""

from fastapi.testclient import TestClient

import psycopg

from api import app

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
    response = client.get("/stores/ArasDjuraffär")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Store ArasDjuraffär not found!'}
    shutdown()


def test_stores_in_list():
    '''
    Testar om angiven affär returnerar rätt namn och address.
    '''
    startup()
    response = client.get("/stores/Djurjouren")
    assert response.status_code == 200
    assert response.json() == {"data": {"name": "Djurjouren",
                               "address": "Upplandsgatan 99, 12345 Stockholm"}}
    shutdown()


def test_stores():
    '''
    Testet returnera data från listan för att se till
    att vi får vad vi förväntar oss
    '''
    startup()
    response = client.get("/stores")
    assert response.status_code == 200
    assert response.json() == {
     "data": [
        {
          "name": "Djurjouren",
          "address": "Upplandsgatan 99, 12345 Stockholm"
        },
        {
          "name": "Djuristen",
          "address": "Skånegatan 420, 54321 Falun"
        },
        {
          "name": "Den Lilla Djurbutiken",
          "address": "Nätverksgatan 22, 55555 Hudiksvall"
        },
        {
          "name": "Den Stora Djurbutiken",
          "address": "Routergatan 443, 54545 Hudiksvall"
        },
        {
          "name": "Noahs Djur & Båtaffär",
          "address": "Stallmansgatan 666, 96427 Gävle"
        }
      ]
    }
    shutdown()


def test_cities():
    """This test checks a call to GET /cities without any query
    parameters.
    """
    startup()
    response = client.get("/cities")
    assert response.status_code == 200
    assert response.json() == {
      "data":
      [
         "Gävle",
         "Falun",
         "Stockholm",
         "Hudiksvall"
      ]
    }
    shutdown()


def test_cities_zip():
    """This test checks a call to GET /cities with a zip query
    added.
    """

    startup()
    response = client.get("/cities?zip=55555")
    assert response.status_code == 200
    assert response.json() == {
      "data": [
        "Hudiksvall"
      ]
    }
    shutdown()


def test_sales():
    """
    Test the respons of GET/sales.
    """

    startup()
    response = client.get("/sales")
    assert response.status_code == 200
    assert response.json() == {
      "data": [
        {
          "store": "Den Stora Djurbutiken",
          "timestamp": "2022-01-25T13:52:34",
          "saleid": "0188146f-5360-408b-a7c5-3414077ceb59"
        },
        {
          "store": "Djuristen",
          "timestamp": "2022-01-26T15:24:45",
          "saleid": "726ac398-209d-49df-ab6a-682b7af8abfb"
        },
        {
          "store": "Den Lilla Djurbutiken",
          "timestamp": "2022-02-07T09:00:56",
          "saleid": "602fbf9d-2b4a-4de2-b108-3be3afa372ae"
        },
        {
          "store": "Den Stora Djurbutiken",
          "timestamp": "2022-02-27T12:32:46",
          "saleid": "51071ca1-0179-4e67-8258-89e34b205a1e"
        }
      ]
    }
    shutdown()


def test_sales_id_valid():
    """
    Tests the return of valid saleid.
    """
    startup()
    response = client.get("/sales/726ac398-209d-49df-ab6a-682b7af8abfb")
    assert response.status_code == 200
    assert response.json() == {
      "data": [
        {
          "store": "Djuristen",
          "timestamp": "2022-01-26T15:24:45",
          "saleid": "726ac398-209d-49df-ab6a-682b7af8abfb",
          "products": [
            {
              "name": "Elefantkoppel",
              "qty": 1
            }
          ]
        }
      ]
    }


def test_sales_id_not_valid():
    """
    Tests the return of s
    """
    startup()
    response = client.get("/sales/726ac398-209d-49df-ab6a-682b7af8")
    assert response.status_code == 422
    assert response.json() == {"detail": "422 Unprocessable entry"}


def test_sales_id_not_exist():
    """
    Tests the return of
    """
    startup()
    response = client.get("/sales/726ac398-209d-49df-ab6a-682b7af8ab80")
    assert response.status_code == 404
    assert response.json() == {"detail": "404 Not found"}
