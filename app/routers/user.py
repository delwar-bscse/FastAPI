from fastapi import  status, Depends, HTTPException, APIRouter
from .. import schemas, models, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/users"
)

# User Part
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == body.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {body.email} already exists")
    hashed_password = utils.hash_password(body.password)
    body.password = hashed_password
    new_user = models.User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 