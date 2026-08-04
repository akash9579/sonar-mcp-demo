import logging
from typing import Any

# Entry point for the FastAPI app
from fastapi import FastAPI
from database import execute_query

from db.repository import find_users_by_name

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/users/search")
async def search_users(query: str):
    logger.info("Received search query: %s", query)
    results = execute_query(query)
    return {"results": results}


@app.get("/users/lookup")
async def lookup_users(name: str) -> dict[str, list[dict[str, Any]]]:
    logger.info("Received lookup request for name: %s", name)
    results = find_users_by_name(name)
    return {"results": results}