from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("basic-auth/")
def login(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }
