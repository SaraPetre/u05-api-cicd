"""api-app
"""


from fastapi import FastAPI

import psycopg

app = FastAPI()


@app.on_event("startup")
def startup():
    """
    a function that should be run before the application starts.
    """
    app.db = psycopg.connect("postgresql://postgres:testpass@localhost/postgres")


@app.on_event("shutdown")
def shutdown():
    """
    a function that should be run when the application is shutting down.
    """
    app.db.close()


@app.get("/stores")
def stores():
    """
    Retrieves a resource from the database.
    """
    with app.db.cursor() as cur:
        cur.execute("SELECT name FROM stores")
        names = cur.fetchall()
        names = [name[0] for name in names]
        return names
