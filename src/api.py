"D"

from fastapi import FastAPI, HTTPException

import psycopg


app = FastAPI()


@app.get("/")
def read_main():
    """The root endpoint, simply says hi to the user :)


    """
    return {"msg": "Hello, World!"}


@app.on_event("startup")
def startup():
    "D"

    app.db = psycopg.connect(
        "dbname=postgres user=postgres host=localhost password=arastest port=5433")


@app.on_event("shutdown")
def shutdown():
    "D"
    app.db.close()


@app.get("/stores/{specifik}")
def specific_store(specifik):
    '''
    returnera data (namn och fullständig address) för en specifik
    butik, vald via namn om ett namn som inte finns i DB anges,
    returnera 404 Not Found
    '''

    with app.db.cursor() as cur:
        cur.execute("""select stores.name, store_addresses.address, store_addresses.zip,
                    store_addresses.city
                    from stores
                    join store_addresses
                    on stores.id = store_addresses.store where name = %s;""", [specifik])
        sname = cur.fetchall()
        if sname:
            sname = sname[0]
            result = {"data": {"name": sname[0], "address": f"{sname[1]}, {sname[2]} {sname[3]}"}}
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Store {specifik} not found!")


@app.get("/stores")
def stores():
    '''
    This endpoint returns data on stores (name and complete adress)
    '''

    with app.db.cursor() as cur:
        cur.execute("""select stores.name, store_addresses.address, store_addresses.zip,
                    store_addresses.city
                    from stores
                    join store_addresses on stores.id = store_addresses.store""")
        for record in cur:
            print(record)
    with app.db.cursor() as cur:
        cur.execute("""select stores.name, store_addresses.address, store_addresses.zip,
                    store_addresses.city
                    from stores
                    join store_addresses on stores.id = store_addresses.store""")
        data = cur.fetchall()
        data = [{"name": d[0], "address": f"{d[1]}, {d[2]} {d[3]}"} for d in data]
        result = {"data": data}
        return result


@app.get("/cities")
def city(zip=None):
    '''
    Denna endpoint returnerar alla unika städer där en butik finns.

    Om query-parameter zip är given, den filtrerar med den och visar
    bara städer med den specifika postkod.
    '''
    with app.db.cursor() as cur:
        if not zip:
            cur.execute("SELECT DISTINCT city FROM store_addresses;")
        else:
            cur.execute("SELECT city FROM store_addresses WHERE zip = %s;", [zip])
        names = cur.fetchall()
        result = {"data": [name[0] for name in names]}
        return result
