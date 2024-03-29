from pydantic import BaseModel, EmailStr, constr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserInDB(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PostBase(BaseModel):
    text: constr(max_length=1048576)  # Maximum length of 1 MB


class PostCreate(PostBase):
    pass


class PostInDB(PostBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class PostID(BaseModel):
    id: int
