from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError

from app.models.user import User
from app.database import get_db


SECRET_KEY=""
ALGORITHM="HS256"
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/login') #extracts token from the profile


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=30)
    
    to_encode.update({
        'exp':expire
    })
    
    token=jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return token

def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload=jwt.decode(token, 
                           SECRET_KEY, 
                           algorithms=[ALGORITHM]
                        )
        id=payload.get("sub")
        
        if not id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        #finding user
        user=db.query(User).filter(User.id==int(id)).first()
        if not user:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        if user.is_deleted:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is pending deletion. Please log in again to reactivate."
            )
        return user
    
    except JWTError:
        raise credentials_exception
        
            