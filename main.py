import base64
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


def _sanitize_for_log(value: str) -> str:
    if value.isalnum():
        return value

    return base64.b64encode(value.encode("utf-8")).decode("ascii")


app = FastAPI()


@app.get("/users/search")
async def search_users(query: str):
    if query.isalnum():
        logger.info("Received search query: %s", query)
    else:
        logger.info("Received search query: Invalid Input: %s", base64.b64encode(query.encode("utf-8")))
    results = execute_query(query)
    return {"results": results}


@app.get("/users/lookup")
async def lookup_users(name: str) -> dict[str, list[dict[str, Any]]]:
    if name.isalnum():
        logger.info("Received lookup request for name: %s", name)
    else:
        logger.info("Received lookup request for name: Invalid Input: %s", base64.b64encode(name.encode("utf-8")))
    results = find_users_by_name(name)
    return {"results": results}


@app.get("/users/find")
async def find_users(name: str) -> dict[str, list[dict[str, Any]]]:
    if name.isalnum():
        logger.info("Received find request for name: %s", name)
    else:
        logger.info("Received find request for name: Invalid Input: %s", base64.b64encode(name.encode("utf-8")))
    results = find_users_by_name(name)
    return {"results": results}


@app.get("/users/filter")
async def filter_users(name: str) -> dict[str, list[dict[str, Any]]]:
    if name.isalnum():
        logger.info("Received filter request for name substring: %s", name)
    else:
        logger.info("Received filter request for name substring: Invalid Input: %s", base64.b64encode(name.encode("utf-8")))
    results = find_users_by_name_substring(name)
    return {"results": results}


@app.get("/users/by-email")
async def get_user_by_email_endpoint(email: str) -> dict[str, dict[str, Any] | None]:
    if email.isalnum():
        logger.info("Received by-email lookup request for email: %s", email)
    else:
        logger.info("Received by-email lookup request for email: Invalid Input: %s", base64.b64encode(email.encode("utf-8")))
    result = get_user_by_email(email)
    return {"result": result}