"""
This is not the greatest project in the world, no.
This is just a tribute!
"""

import uuid
from collections import namedtuple
from typing import List, Optional

import psycopg
from fastapi import FastAPI, Query, HTTPException


app = FastAPI()


@app.on_event("startup")
def startup():
    '''
    Open database connection
    '''
    app.db = psycopg.connect(
        """dbname=u05 user=postgres host=doe21-db.grinton.dev
         password=DjExUSMcwWpzXziT port=5432""") # pragma: no cover


@app.on_event("shutdown")
def shutdown():
    '''
    Close database connection
    '''
    app.db.close() # pragma: no cover


@app.get("/")
def main():
    '''
    Returns a welcome message
    '''
    return {"msg": "Hello, World!"}


@app.get("/stores")
def stores():
    '''
    This endpoint returns data on stores (name and complete adress)
    '''
    with app.db.cursor() as cur:
        cur.execute('''SELECT stores.name, store_addresses.address,
                    store_addresses.zip, store_addresses.city
                    FROM stores JOIN store_addresses on stores.id
                    = store_addresses.store;
                    ''')
        data = cur.fetchall()
        data = [{"name": d[0], "address": f"{d[1]}, {d[2]} {d[3]}"}
                for d in data]
        result = {"data": data}
        return result


@app.get("/stores/{storename}")
def specific_store(storename=None):
    '''
    Returns store name and address for a specific store chosen by name,
    if no/wrong name is given return 404 Not Found.
    '''

    with app.db.cursor() as cur:
        cur.execute("""select stores.name, store_addresses.address,
                    store_addresses.zip, store_addresses.city
                    from stores
                    join store_addresses
                    on stores.id = store_addresses.store where name
                    = %s;""", [storename])
        sname = cur.fetchall()
        if not sname:
            raise HTTPException(status_code=404, detail=f'Store {storename} not found!')

        if sname:
            sname = sname[0]
            result = {"data": {"name": sname[0],
                      "address": f"{sname[1]}, {sname[2]} {sname[3]}"}}
            return result
        return None


@app.get("/cities")
def city(zipcode=None):
    '''
    This endpoint returns data on all unique cities where a store
    is located. The query can be filtered if a zip-parameter is given.
    '''
    with app.db.cursor() as cur:
        if not zipcode:
            cur.execute("SELECT DISTINCT city FROM store_addresses;")
        else:
            cur.execute("SELECT city FROM store_addresses WHERE zip\
                        = %s;", [zipcode])
        names = cur.fetchall()
        result = {"data": [name[0] for name in names]}
        return result


@app.get("/sales")
def sales():
    '''
    Returns storename, time, saleid
    '''
    with app.db.cursor() as cur:
        cur.execute("""SELECT stores.name, sales.time, sales.id
                    FROM stores
                    JOIN sales
                    ON stores.id = sales.store;""")
        dbdata = cur.fetchall()
    data = []
    for items in dbdata:
        name, date_time, sale_id = items
        date_time = str(date_time).replace(" ", "T").replace("-", "")
        data.append({"store": name, "timestamp": date_time,
                    "sale_id": str(sale_id)})
    return {"data": data}


@app.get("/sale/{saleid}")
def sale(saleid=None):
    '''
    Returns store name,date/time,saleid, product name and quantity for
    a specific sale..
    '''
    try:
        uuid.UUID(saleid)
    except ValueError as err:
        raise HTTPException(status_code=422,
                            detail="422 Unprocessable entry") from err

    with app.db.cursor() as cur:
        cur.execute("""SELECT stores.name, sales.time, sales.id,
                    sold_products.quantity, products.name
                    FROM sales
                    INNER JOIN stores ON stores.id = sales.store
                    INNER JOIN sold_products ON sales.id
                    = sold_products.sale
                    INNER JOIN products ON products.id
                    = sold_products.product
                    where sales.id = %s;""", [saleid])
        dbdata = cur.fetchall()
        if not dbdata:
            raise HTTPException(status_code=404, detail="404 Not found")
        data = []
        data_for_products = []
        for items_in_data in dbdata:
            store_name, timestamp, sale_id, quantity, produkt_name = items_in_data
            timestamp = str(timestamp).replace(" ", "T").replace("-", "")
            data_for_products.append({"name": produkt_name, "qty": quantity})
            data.append({"store": store_name, "timestamp": timestamp,
                         "saleid": sale_id, "products": data_for_products})
        return {"data": data[0]}


@app.get("/income")
def get_income(store: Optional[List[str]] = Query(None),
               product: Optional[List[str]] = Query(None),
               from_=Query(None, alias="from"), to_=Query(None, alias="to")):
    """GET /income

    Returns data in the usual format {"data": ·list-of-dicts}. Each
    dictionary contains all info about a transaction, including price and
    discount percent.

    It accepts the following query parameters:
        - store: (can be given more than once) UUID to filter results by store
        - product: (can be given more than once) UUID to filter results by
          product
        - from: filter out all transactions before the given datestamp/timestamp
        - to: filter out all transactions after the given datestamp/timestamp

    If any invalid UUID is given (either in store or product), 422 -
    Unprocessable Entity will be returned
    """
    stores_clause, products_clause, from_clause, to_clause = "", "", "", ""
    parameters = []
    if store:
        try:
            for iterator in store:
                uuid.UUID(iterator)
        except ValueError as err:
            raise HTTPException(status_code=422,
                                detail="Invalid UUID given for store!") from err
        stores_clause = "WHERE stores.id = ANY(%s)"
        parameters.append(store)
    if product:
        try:
            for iterator in product:
                uuid.UUID(iterator)
        except ValueError as err:
            raise HTTPException(
                status_code=422,
                detail="Invalid UUID given for product!") from err
        products_clause = "WHERE products.id = ANY(%s)"
        if parameters:
            products_clause = products_clause.replace("WHERE", "AND")
        parameters.append(product)
    if from_:
        from_clause = "WHERE sales.time >= %s"
        if parameters:
            from_clause = from_clause.replace("WHERE", "AND")
        parameters.append(from_)
    if to_:
        to_clause = "WHERE sales.time <= %s"
        if parameters:
            to_clause = to_clause.replace("WHERE", "AND")
        parameters.append(to_)
    query = """SELECT stores.name, products.name, prices.price,
               sold_products.quantity, sales.time, discounts.discount_percent
               FROM sold_products 
               JOIN products on sold_products.product = products.id 
               JOIN sales ON sold_products.sale = sales.id 
               JOIN stores ON sales.store = stores.id 
               JOIN prices ON products.id = prices.product
               LEFT JOIN discounts ON products.id = discounts.product
               {stores} {products} {from_} {to}
               ORDER BY sales.time;"""
    query = query.format(stores=stores_clause, products=products_clause,
                         from_=from_clause, to=to_clause)
    try:
        with app.db.cursor() as cur:
            cur.execute(query, parameters)
            result = cur.fetchall()
    except psycopg.errors.Error:
        app.db.rollback()
        raise HTTPException(status_code=422, detail="Invalid datetime format!")
    entries = [QueryResultIncome(*r)._asdict() for r in result]
    return {"data": entries}


# QueryResultInventory is a named tuple used to ease the parsing of
# list-of-lists data format returned by cursor.fetchall into dictionaries
# ready to be returned as JSON.
QueryResultInventory = namedtuple("QueryResultInventory", ("product_name",
                                                           "adjusted_quantity",
                                                           "store_name"))
