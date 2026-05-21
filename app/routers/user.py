from fastapi import  status, Response, Depends, HTTPException, APIRouter
from .. import schemas, models, utils
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/users"
)

# User Part
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {user.email} already exists")
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 