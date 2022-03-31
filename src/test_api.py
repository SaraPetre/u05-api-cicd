"""Minimal tests for api.py
"""

from types import SimpleNamespace

import psycopg
from fastapi.testclient import TestClient

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


def test_get_income():
    '''
    The test returnes status code 200 and data when NO query is used.
    '''
    startup()
    response = client.get("/income")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Sömnpiller och energidryck för djur",
                "price": 9.95,
                "quantity": 12,
                "sale_time": "2022-01-25T13:52:34",
                "discount": 9
            },
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Hundmat",
                "price": 109,
                "quantity": 3,
                "sale_time": "2022-01-25T13:52:34",
                "discount": None
            },
            {
                "store_name": "Djuristen",
                "product_name": "Elefantkoppel",
                "price": 459,
                "quantity": 1,
                "sale_time": "2022-01-26T15:24:45",
                "discount": 13
            },
            {
                "store_name": "Den Lilla Djurbutiken",
                "product_name": "Kattmat",
                "price": 109,
                "quantity": 57,
                "sale_time": "2022-02-07T09:00:56",
                "discount": None
            },
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Kattklonare",
                "price": 55900,
                "quantity": 1,
                "sale_time": "2022-02-27T12:32:46",
                "discount": 25
            },
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Kattmat",
                "price": 109,
                "quantity": 10,
                "sale_time": "2022-02-27T12:32:46",
                "discount": None
            }
        ]
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


def test_get_income_valid_products_uuid():
    '''
    The test returnes status code 200 and data for products
    '''
    startup()
    response = client.get("/income?product=19e67404-6e35-45b7-8d6f-e5bc5b79c453")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Kattklonare",
                "price": 55900,
                "quantity": 1,
                "sale_time": "2022-02-27T12:32:46",
                "discount": 25
            }
        ]
    }
    shutdown()


def test_get_income_two_valid_products_uuid():
    '''
    The test returnes status code 200 and data for products
    '''
    startup()
    response = client.get("/income?product=19e67404-6e35-45b7-8d6f-e5bc5b79c453&"
                          "product=eb4d618c-122d-4428-b022-38aa1ad36fe0")
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
            },
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Kattklonare",
                "price": 55900,
                "quantity": 1,
                "sale_time": "2022-02-27T12:32:46",
                "discount": 25
            }
        ]
    }
    shutdown()


def test_get_income_not_valid_product_uuid():
    '''
    The test returnes status code 422 if we give an invalid UUID for store Djuristen.
    '''
    startup()
    response = client.get("/income?product=19e67404-6e35-45b7-8d6f-e5bc5b79c4511")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid UUID given for product!"}
    shutdown()


def test_get_income_from():
    '''
    The test returnes status code 200 and data when query from is used.
    '''
    startup()
    response = client.get("/income?from=2022-01-26")
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
            },
            {
                "store_name": "Den Lilla Djurbutiken",
                "product_name": "Kattmat",
                "price": 109,
                "quantity": 57,
                "sale_time": "2022-02-07T09:00:56",
                "discount": None
            },
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Kattklonare",
                "price": 55900,
                "quantity": 1,
                "sale_time": "2022-02-27T12:32:46",
                "discount": 25
            },
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Kattmat",
                "price": 109,
                "quantity": 10,
                "sale_time": "2022-02-27T12:32:46",
                "discount": None
            }
        ]
    }
    shutdown()


def test_get_income_not_valid_datetime():
    '''
    The test returnes status code 422 if we give an invalid datetime.
    '''
    startup()
    response = client.get("/income?from=22-02-07T09%3A00%3A56")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid datetime format!"}
    shutdown()


def test_get_income_to():
    '''
    The test returns a list of all sales with a sale time
    up to the given sale time.
    '''
    startup()
    response = client.get("/income?to=2022-01-26")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Sömnpiller och energidryck för djur",
                "price": 9.95,
                "quantity": 12,
                "sale_time": "2022-01-25T13:52:34",
                "discount": 9
            },
            {
                "store_name": "Den Stora Djurbutiken",
                "product_name": "Hundmat",
                "price": 109,
                "quantity": 3,
                "sale_time": "2022-01-25T13:52:34",
                "discount": None
            }
        ]
    }


all_inventories = [
    [
        "Hundmat",
        27,
        "Den Lilla Djurbutiken"
    ],
    [
        "Kattmat",
        387,
        "Den Lilla Djurbutiken"
    ],
    [
        "Hundmat",
        140,
        "Den Stora Djurbutiken"
    ],
    [
        "Kattklonare",
        68,
        "Den Stora Djurbutiken"
    ],
    [
        "Kattmat",
        643,
        "Den Stora Djurbutiken"
    ],
    [
        "Sömnpiller och energidryck för djur",
        61,
        "Den Stora Djurbutiken"
    ],
    [
        "Elefantkoppel",
        27,
        "Djuristen"
    ],
]

return_data = [
    {
        "product_name": "Hundmat",
        "adjusted_quantity": 27,
        "store_name": "Den Lilla Djurbutiken"
    },
    {
        "product_name": "Kattmat",
        "adjusted_quantity": 387,
        "store_name": "Den Lilla Djurbutiken"
    },
    {
        "product_name": "Hundmat",
        "adjusted_quantity": 140,
        "store_name": "Den Stora Djurbutiken"
    },
    {
        "product_name": "Kattklonare",
        "adjusted_quantity": 68,
        "store_name": "Den Stora Djurbutiken"
    },
    {
        "product_name": "Kattmat",
        "adjusted_quantity": 643,
        "store_name": "Den Stora Djurbutiken"
    },
    {
        "product_name": "Sömnpiller och energidryck för djur",
        "adjusted_quantity": 61,
        "store_name": "Den Stora Djurbutiken"
    },
    {
        "product_name": "Elefantkoppel",
        "adjusted_quantity": 27,
        "store_name": "Djuristen"
    }
]


def db_mock(data):
    """This function returns a database mocking object, that will be used
    instead of the actual db connection.
    """
    database = SimpleNamespace()
    database.cursor = CursorMock(data)
    return database


class CursorMock:
    """This class mocks a db cursor. It does not build upon unittest.mock but
    it is instead built from an empty class, patching manually all needed
    methods.
    """
    def __init__(self, data):
        self.data = data

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __call__(self):
        return self

    @staticmethod
    def execute(*args):
        """This mocks cursor.execute. It returns args even though the return
        value of cursor.execute() is never used. This is to avoid the
        following linting error:

        W0613: Unused argument 'args' (unused-argument)
        """
        return args

    def fetchall(self):
        """This mocks cursor.fetchall.
        """
        return self.data


def test_get_inventory():
    """This unit test checks a call to GET /inventory without any query
    parameters.
    """
    app.db = db_mock(all_inventories)
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json() == return_data


def test_get_inventory_store():
    """This unit test checks a call to GET /inventory?store=UUID
    """
    data = list(filter(lambda x: x[-1] == "Den Stora Djurbutiken",
                       all_inventories))
    app.db = db_mock(data)
    response = client.get("/inventory",
                          params={
                              "store": "676df1a1-f1d1-4ac5-9ee3-c58dfe820927"})
    assert response.status_code == 200
    assert response.json() == list(filter(
        lambda x: x["store_name"] == "Den Stora Djurbutiken", return_data))


def test_get_inventory_product():
    """This unit test checks a call to GET /inventory?product=UUID
    """
    data = list(filter(lambda x: x[0] == "Hundmat", all_inventories))
    app.db = db_mock(data)
    response = client.get("/inventory",
                          params={
                              "product": "a37c34ae-0895-484a-8b2a-355aea3b6c44"
                          })
    assert response.status_code == 200
    assert response.json() == list(filter(
        lambda x: x["product_name"] == "Hundmat", return_data))


def test_get_inventory_store_and_product():
    """This unit test checks a call to GET /inventory?store=UUID&product=UUID
    """
    data = list(filter(
        lambda x: x[0] == "Hundmat" and x[-1] == "Den Stora Djurbutiken",
        all_inventories))
    app.db = db_mock(data)
    response = client.get("/inventory", params={
        "product": "a37c34ae-0895-484a-8b2a-355aea3b6c44",
        "store": "676df1a1-f1d1-4ac5-9ee3-c58dfe820927"
    })
    assert response.status_code == 200
    assert response.json() == list(
        filter(
            lambda x: x["store_name"] == "Den Stora Djurbutiken" and x["product_name"
                                    ] == "Hundmat", return_data))


def test_get_inventory_erroneous_store():
    """This unit test checks for a call to GET /inventory?store=Erroneous-UUID
    """
    app.db = db_mock(None)
    response = client.get("/inventory",
                          params={"store": "this is not a valid UUID!"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid UUID for store!"}


def test_get_inventory_erroneous_product():
    """This unit test checks for a call to GET /inventory?product=Erroneous-UUID
    """
    app.db = db_mock(None)
    response = client.get("/inventory",
                          params={"product": "this is not a valid UUID!"})
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid UUID for product!"}
