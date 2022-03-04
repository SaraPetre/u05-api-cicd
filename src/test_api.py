"D"
from fastapi import FastAPI

import psycopg

app = FastAPI()


@app.on_event("startup")
def startup():
    "D"
    app.db = psycopg.connect(
        "postgresql://postgres:arastest@localhost/postgres")


@app.on_event("shutdown")
def shutdown():
    "D"
    app.db.close()


@app.get("/stores")
def stores():
    "D"
    with app.db.cursor() as cur:
        cur.execute("SELECT name FROM stores")
        names = cur.fetchall()
        names = [name[0] for name in names]
        return names
