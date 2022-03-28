"""
This is not the greatest project in the world, no.
This is just a tribute!
"""

import uuid

import psycopg
from fastapi import FastAPI, HTTPException


app = FastAPI()


@app.on_event("startup")
def startup():
    '''
    Open database connection
    '''
    app.db = psycopg.connect(
        """dbname=u05 user=postgres host=doe21-db.grinton.dev
         password=DjExUSMcwWpzXziT port=5432""")
    # postgresql://postgres:DjExUSMcwWpzXziT@doe21-db.grinton.dev/u05


@app.on_event("shutdown")
def shutdown():
    '''
    Close database connection
    '''
    app.db.close()


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
