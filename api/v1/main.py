#!/usr/bin/python3
"""Estate planning software entry file."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.configurations.database import engine
from api.v1.models.data.users import Base as UserBase
from api.v1.models.data.assets import Base as AssetBase
from api.v1.routes.users import user_routers
from api.v1.routes.trustees import trustee_router
from api.v1.routes.beneficiaries import beneficiary_router
from api.v1.routes.assets import asset_router

UserBase.metadata.create_all(bind=engine)
AssetBase.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]
# Cors middleware settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index() -> dict[str, str]:
    """Entry point for EstateTrust."""
    return {
        "message": "Welcome to Estate Trust."
    }


app.include_router(user_routers)
app.include_router(trustee_router)
app.include_router(beneficiary_router)
app.include_router(asset_router)
