from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# from pydantic import BaseModel

# class Book(BaseModel):
#     title: str
#     author: str
#     year: int
