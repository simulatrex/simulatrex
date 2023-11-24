from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server import schemas, dependencies
from server.crud import user as crud

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    return crud.create_user(db=db, user=user)
