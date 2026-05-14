from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):

    name: str = Field(min_length=3)

    email: EmailStr

    password: str = Field(min_length=6)
    
    role: str = Field(default="user")


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: str

    class Config:
        orm_mode = True