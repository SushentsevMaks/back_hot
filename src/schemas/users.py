from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str

class UserAdd(BaseModel):
    email: str
    hashed_password: str

class User(BaseModel):
    id: int
    email: str

