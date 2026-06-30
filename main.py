from fastapi import FastAPI
from database import execute_query

app = FastAPI()

@app.get("/users/search")
async def search_users(query: str):
    results = execute_query(query)
    return {"results": results}