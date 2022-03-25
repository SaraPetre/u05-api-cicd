import uuid
from datetime import datetime
# from collections import namedTuple
# from typing import List, Optional

import psycopg
from fastapi import FastAPI, Query, HTTPException


app = FastAPI()


@app.on_event("startup")
def startup():
    '''
    fillertext
    '''
    app.db = psycopg.connect(
    "postgresql://postgres:DjExUSMcwWpzXziT@doe21-db.grinton.dev/u05"
    )


@app.on_event("shutdown")
def shutdown():
    '''
    fillertext
    '''
    app.db.close()


@app.get("/sales_test")
def sales():
    '''
    GET /sales : Denna endpoint ska returnera en lista över alla transak-
    tioner, i denna format:
    {” data ”:[
    {”store”:”Storename”,
    ”timestamp”:”yyyymmddThh:mm:ss”,
    ”saleid”:”uuid=for=the=transaction=here”},
    ...
    ]
    }
    '''
    # 2022-01-25T13:52:34
    # Saknar tidsformattering

    with app.db.cursor() as cur:
        cur.execute("""SELECT stores.name, sales.time, sales.id
                    FROM stores
                    JOIN sales
                    ON stores.id = sales.store;""")
        dbdata = cur.fetchall()
    data = []
    for x in dbdata:
        name, date_time, sale_id = x
        date_time = datetime.strptime(str(date_time), "%Y-%m-%dT%H:%M:%S")
        date_time = datetime.strftime("%Y%m%dT%H:%M:%S")
        data.append({"store": name, "timestamp": date_time, 
                    "sale_id": str(sale_id)})

    return {"data": data}


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
           raise HTTPException(status_code=404,
                            detail="404 Not found")

        if sname:
            sname = sname[0]
            result = {"data": {"name": sname[0],
                        "address": f"{sname[1]}, {sname[2]} {sname[3]}"}}
            return result


@app.get("/cities")
def city(zip=None):
    '''
    This endpoint returns data on all unique cities where a store
    is located. The query can be filtered if a zip-parameter is given.
    '''
    with app.db.cursor() as cur:
        if not zip:
            cur.execute("SELECT DISTINCT city FROM store_addresses;")
        else:
            cur.execute("SELECT city FROM store_addresses WHERE zip\
                        = %s;", [zip])
        names = cur.fetchall()
        result = {"data": [name[0] for name in names]}
        return result


@app.get("/sales")
def sales():
    """Returns storename, time,saleid"""

    # Saknar tidsformattering

    with app.db.cursor() as cur:
        cur.execute("""SELECT stores.name, sales.time, sales.id
                    FROM stores
                    JOIN sales
                    ON stores.id = sales.store;""")
        data = cur.fetchall()
        data = {"data": [{"store": d[0], "timestamp": d[1],
                "saleid": d[2]} for d in data]}
        return data


@app.get("/sales/{saleid}")
def sales(saleid=None):
    '''
    Returns store name,date/time,saleid, product name and quantity for
    a specific sale.    
    '''

    # saknar tidsformattering

    try:
        uuid.UUID(saleid)
    except ValueError:
        raise HTTPException(status_code=422,
                            detail="422 Unprocessable entry")

    with app.db.cursor() as cur:
        cur.execute("""SELECT stores.name, sales.time, sales.store,
                    sales.id,sold_products.product,
                    sold_products.quantity, products.name
                    FROM sales
                    INNER JOIN stores ON stores.id = sales.store
                    INNER JOIN sold_products ON sales.id
                    = sold_products.sale
                    INNER JOIN products ON products.id
                    = sold_products.product
                    where sold_products.sale = %s;""", [saleid])
        data = cur.fetchall()
        if not data:
           raise HTTPException(status_code=404,
                            detail="404 Not found")

        data = {"data":[{"store": d[0], "timestamp": d[1], "saleid": d[3],
                "products":[{ "name": d[6], "qty": d[5]}]
                }
                for d in data]}
        return data
