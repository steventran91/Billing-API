from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db 
from ..models.user import User
from ..schemas.user import LoginRequest, TokenResponse
from ..core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
   
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    
    confirm_password = verify_password(request.password, user.hashed_password)
    if not confirm_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password", headers={"WWW-Authenticate": "Bearer"})

    payload = {"user_id": user.id, "role": "user"}
    token = create_access_token(payload)
    return TokenResponse(access_token=token, token_type="bearer")
    
  