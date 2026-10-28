import hmac
import logging
import os
from typing import Any

# Entry point for the FastAPI app
from fastapi import Depends, FastAPI, Header, HTTPException

from db.repository import (
    find_users_by_name,
    find_users_by_name_substring,
    get_user_by_email,
)

logger = logging.getLogger(__name__)

app = FastAPI()


def require_authenticated_caller(
    authorization: str | None = Header(default=None),
) -> None:
    expected_token = os.environ.get("API_AUTH_TOKEN")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    provided_token = authorization.removeprefix("Bearer ")
    if not expected_token or not hmac.compare_digest(provided_token, expected_token):
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/users/search", dependencies=[Depends(require_authenticated_caller)])
async def search_users(query: str) -> dict[str, list[dict[str, Any]]]:
    logger.info("Received search query: %s", query)
    results = find_users_by_name(query)
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