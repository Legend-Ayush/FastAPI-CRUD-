from pydantic import BaseModel, EmailStr, BeforeValidator
from typing import Annotated, Literal


def to_lower(v: str) -> str:
    return v.strip().lower() if isinstance(v, str) else v


def name_title(v: str) -> str:
    return v.strip().title() if isinstance(v, str) else v


NormalizedEmail = Annotated[
    EmailStr,
    BeforeValidator(to_lower)
]

NormalizedName = Annotated[
    str,
    BeforeValidator(name_title)
]


class UserCreate(BaseModel):
    name: NormalizedName
    email: NormalizedEmail
    password: str


class UserResponse(BaseModel):
    id: int
    name: NormalizedName
    email: NormalizedEmail

    class Config: #Converts reponse from the databse directly into JSON
        from_attributes = True


class UserLogin(BaseModel):
    email: NormalizedEmail
    password: str


class DeleteUserResponse(BaseModel):
    message: str
    name: NormalizedName


class UserUpdate(BaseModel):
    current_password: str

    name: NormalizedName | None = None
    email: NormalizedEmail | None = None
    new_password: str | None = None


class UserReactivate(BaseModel):
    email: Annotated[
        EmailStr,
        BeforeValidator(lambda v: v.strip().lower())
    ]

    current_password: str


class TokenResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"]


class RefreshResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]