from pydantic import BaseModel, EmailStr, BeforeValidator, Field
from typing import Annotated, Literal

class UserCreate(BaseModel):
    name: Annotated[
        str,
        BeforeValidator(lambda v: v.strip().title()),
        Field(..., min_length=1, max_length=100)
    ]
    email: Annotated[
        EmailStr,
        BeforeValidator(lambda v: v.strip().lower()),
        Field(..., max_length=500)
    ]
    password: Annotated[
        str,
        Field(..., min_length=8)
    ]

class UserResponse(BaseModel):
    id: int
    name: Annotated[
        str,
        BeforeValidator(lambda v: v.strip().title())
    ]
    email: Annotated[
        EmailStr,
        BeforeValidator(lambda v: v.strip().lower())
    ]
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: Annotated[
        EmailStr,
        BeforeValidator(lambda v: v.strip().lower()),
        Field(..., max_length=500)
    ]
    password: Annotated[
        str,
        Field(..., min_length=1)
    ]

class DeleteUserResponse(BaseModel):
    message: str
    name: Annotated[
        str,
        BeforeValidator(lambda v: v.strip().title())
    ]

class UserUpdate(BaseModel):
    current_password: Annotated[
        str,
        Field(..., min_length=1)
    ]
    name: Annotated[
        str | None,
        BeforeValidator(lambda v: v.strip().title() if v is not None else None),
        Field(default=None, min_length=1, max_length=100)
    ]
    email: Annotated[
        EmailStr | None,
        BeforeValidator(lambda v: v.strip().lower() if v is not None else None),
        Field(default=None, max_length=500)
    ]
    new_password: Annotated[
        str | None,
        Field(default=None, min_length=8)
    ]

class UserReactivate(BaseModel):
    email: Annotated[
        EmailStr,
        BeforeValidator(lambda v: v.strip().lower()),
        Field(..., max_length=500)
    ]
    current_password: Annotated[
        str,
        Field(..., min_length=1)
    ]

class TokenResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"]

class RefreshResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]

class LogoutResponse(BaseModel):
    message: str