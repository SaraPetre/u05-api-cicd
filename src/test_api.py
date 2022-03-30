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
    assert response.json() == {"detail": 'Store ArasDjuraffär not found!'}
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


def test_cities():
    """This test checks a call to GET /cities without any query
    parameters.
    """
    startup()
    response = client.get("/cities")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
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
    response = client.get("/cities?zipcode=55555")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            "Hudiksvall"
        ]
    }
    shutdown()


def test_stores():
    """
    Test the respons of GET/sales.
    """

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
                "timestamp": "20220125T13:52:34",
                "sale_id": "0188146f-5360-408b-a7c5-3414077ceb59"
            },
            {
                "store": "Djuristen",
                "timestamp": "20220126T15:24:45",
                "sale_id": "726ac398-209d-49df-ab6a-682b7af8abfb"
            },
            {
                "store": "Den Lilla Djurbutiken",
                "timestamp": "20220207T09:00:56",
                "sale_id": "602fbf9d-2b4a-4de2-b108-3be3afa372ae"
            },
            {
                "store": "Den Stora Djurbutiken",
                "timestamp": "20220227T12:32:46",
                "sale_id": "51071ca1-0179-4e67-8258-89e34b205a1e"
            }
        ]
    }
    shutdown()


def test_sales_id_valid():
    """
    Tests the return of valid saleid.
    """
    startup()
    response = client.get("/sale/726ac398-209d-49df-ab6a-682b7af8abfb")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "store": "Djuristen",
            "timestamp": "20220126T15:24:45",
            "saleid": "726ac398-209d-49df-ab6a-682b7af8abfb",
            "products": [
                {
                    "name": "Elefantkoppel",
                    "qty": 1
                }
            ]
        }
    }


def test_sales_id_not_valid():
    """
    Tests the return of s
    """
    startup()
    response = client.get("/sale/726ac398-209d-49df-ab6a-682b7af8")
    assert response.status_code == 422
    assert response.json() == {"detail": "422 Unprocessable entry"}


def test_sales_id_not_exist():
    """
    Tests the return of
    """
    startup()
    response = client.get("/sale/726ac398-209d-49df-ab6a-682b7af8ab80")
    assert response.status_code == 404
    assert response.json() == {"detail": "404 Not found"}


def test_sales_id_store_two_products():
    """
    Tests the return of two valid saleids.
    """
    startup()
    response = client.get("/sale/0188146f-5360-408b-a7c5-3414077ceb59")
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "store": "Den Stora Djurbutiken",
            "timestamp": "20220125T13:52:34",
            "saleid": "0188146f-5360-408b-a7c5-3414077ceb59",
            "products": [
                {
                    "name": "Hundmat",
                    "qty": 3
                },
                {
                    "name": "Sömnpiller och energidryck för djur",
                    "qty": 12
                }
            ]
        }
    }


def test_get_income_one_store():
    '''
    The test returnes status code 200 if we get the result wanted for store Djuristen.
    '''
    startup()
    response = client.get("/income?store=75040436-56de-401b-8919-8d0063ac9dd7")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "store_name": "Djuristen",
                "product_name": "Elefantkoppel",
                "price": 459,
                "quantity": 1,
                "sale_time": "2022-01-26T15:24:45",
                "discount": 13
            }
        ]
    }
    shutdown()


def test_get_income_not_valid_store_uuid():
    '''
    The test returnes status code 422 if we give an invalid UUID for store Djuristen.
    '''
    startup()
    response = client.get("/income?store=75040436-56de-401b-8919-8d0063ac9d")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid UUID given for store!"}
    shutdown()
