import logging
from typing import Any

# Entry point for the FastAPI app
from fastapi import FastAPI
from database import execute_query

from db.repository import (
    find_users_by_name,
    find_users_by_name_substring,
    get_user_by_email,
)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/users/search")
async def search_users(query: str):
    logger.info("Received search request")
    results = execute_query(query)
    return {"results": results}


@app.get("/users/lookup")
async def lookup_users(name: str) -> dict[str, list[dict[str, Any]]]:
    logger.info("Received lookup request for name: %s", name)
    results = find_users_by_name(name)
    return {"results": results}


@app.get("/users/find")
async def find_users(name: str) -> dict[str, list[dict[str, Any]]]:
    logger.info("Received find request for name: %s", name)
    results = find_users_by_name(name)
    return {"results": results}


@app.get("/users/filter")
async def filter_users(name: str) -> dict[str, list[dict[str, Any]]]:
    logger.info("Received filter request for name substring: %s", name)
    results = find_users_by_name_substring(name)
    return {"results": results}


@app.get("/users/by-email")
async def get_user_by_email_endpoint(email: str) -> dict[str, dict[str, Any] | None]:
    logger.info("Received by-email lookup request for email: %s", email)
    result = get_user_by_email(email)
    return {"result": result}