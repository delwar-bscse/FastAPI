from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2, schemas
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
  prefix="/auth",
  tags=["Authentication"]
)

@router.post("/login", response_model=schemas.UserLogin)
def login(body: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {body.username} not found")
    if not utils.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Incorrect password")
    
    access_token = oauth2.create_access_token(
        data = {"user_id": user.id},
        expires_delta = timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "user": user
    }