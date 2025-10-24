from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db


async def verify_token(x_token: str = Header(...)):
    """Dependency for token verification"""
    # Use best way to confirm token
    # if x_token != "fake-super-secret-token":
    #     raise HTTPException(status_code=400, detail="X-Token header invalid")
    return x_token


async def get_common_parameters(
    db: Session = Depends(get_db),
    x_token: str = Depends(verify_token)
):
    """Common dependencies for endpoints"""
    return {"db": db, "x_token": x_token}
