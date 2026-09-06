from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin, DeleteUserResponse, UserUpdate
from app.utils.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_existing = db.execute(
        select(User).where(User.email == user_data.email)
    ).scalar_one_or_none()
    
    if user_existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User already exists with this email'
        )
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hash_password=hash_password(user_data.password)
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not register user"
        ) 

@router.post('/login')
def login(user:UserLogin, db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email and password'
        )
    
    #password verify
    is_valid=verify_password(user.password,db_user.hash_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email and password"
        )
    
    if db_user.is_deleted:
        db_user.is_deleted=False
        db_user.schedule_delete_at=None
        db.commit()
    
    #token generate
    data={"sub":str(db_user.id)}
    access_token=create_access_token(data)
        
    return{
        'message':'Login Successfully',
        'access_token':access_token,
        'token_type':'bearer' # Here, 'bearer' indicates that the token is a bearer token, which means that the client must include it in the Authorization header of subsequent requests to access protected resources.
    }

@router.get('/profile')
def profile(current_user:User=Depends(get_current_user)): #Runs Dependency injection to extract token
    return{
        'id': current_user.id,
        'email':current_user.email,
        'name':current_user.name
    }

@router.delete("/delete", response_model=DeleteUserResponse, status_code=status.HTTP_200_OK
)
def delete(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account already pending for deletion"
        )

    user_name = current_user.name

    try:
        current_user.is_deleted = True
        current_user.schedule_delete_at = (
            datetime.now(timezone.utc) + timedelta(days=30)
        )

        db.commit()
        formatted_date = current_user.schedule_delete_at.strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )

        return DeleteUserResponse(
            message=f"Account deletion scheduled for {formatted_date}",
            name=user_name
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not schedule account deletion"
        )

@router.patch('/update', status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(user_update:UserUpdate,
                current_user:User=Depends(get_current_user),
                db:Session=Depends(get_db)):
    
    if not verify_password(user_update.current_password, current_user.hash_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    changes=user_update.model_dump(exclude_unset=True)
    
    if "email" in changes:
        if changes["email"]!=current_user.email:
            existing_user=db.query(User).filter(
                User.email==changes["email"],
                User.id!=current_user.id
            ).first()
            
            if existing_user: 
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use by another user"
                )
        
            current_user.email=changes["email"]
    
    if "new_password" in changes:
        current_user.hash_password=hash_password(changes["new_password"])
    
    if "name" in changes:
        current_user.name=changes["name"]
    
    try:
        db.commit()
        db.refresh(current_user)
        return current_user
    
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )