from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {"db": "connected"}
