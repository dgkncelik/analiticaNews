from typing import Union
from fastapi import FastAPI
import uvicorn
import sqlite3
import sql_functions

app = FastAPI()

API_DB_NAME = "scrape_database.db"
API_ELASTIC_URL = "http://54.85.90.67:9200"
conn = sqlite3.connect(API_DB_NAME, check_same_thread=False)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/haberler/")
def get_all_news():
    news = []
    result = sql_functions.read_all_news(conn)
    for r in result:
        n = {
            "id": r[0],
            "title": r[1],
            "date": r[2],
            "summary": r[4],
            "link": r[3],
            "author": r[5]
        }

        news.append(n)

    return {"haberler": news}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)