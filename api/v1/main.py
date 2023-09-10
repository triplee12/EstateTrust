#!/usr/bin/python3
"""Estate planning software entry file."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index() -> dict[str, str]:
    """Entry point for EstateTrust."""
    return {
        "message": "Welcome to Estate Trust."
    }
