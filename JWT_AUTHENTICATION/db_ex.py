from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from hash_ex import hash_password, verify_password
from jwt_utils import create_access_token, verify_token

# declarative_base() is a factory function
# it will track all tables that we create using the Base class
# it is manager of the database tables and their relationships
Base = declarative_base()

app = FastAPI()

class Users(Base): 
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True) 
    name = Column(String) 
    email = Column(String) 
    password = Column(String)

from pydantic import BaseModel, EmailStr, Field
class UserCreate(BaseModel):
    name: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

DB_URL = "postgresql://postgres:password@localhost:5432/postgres"

engine = create_engine(DB_URL)  # Connect to the database
Session = sessionmaker(bind=engine)

# Create the tables in the database
Base.metadata.create_all(engine)


# To get the database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(
        Users.email == user.email).first()

    # Checking if the user exists in the database
    if not db_user:
        raise HTTPException(status_code=400, 
                            detail="User not found")

    # Verifying password
    verified = verify_password(user.password, 
                               db_user.password)
    if not verified:
        raise HTTPException(status_code=400, 
                            detail="Invalid password")

    access_token = create_access_token(
        {
            "user_id": db_user.id,
            "email": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # this line creates a new instance of the Users
    # model using the data from the UserSchema
    new_user = Users(
        name=user.name, email=user.email, password=hash_password(user.password)
    )
    db.add(new_user)  # Add the new user to the session
    # Save the changes to the database
    db.commit()
    db.refresh(new_user)
    return new_user


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.id == user_id).first()
    if not existing_user:
        return {"error": "User not found"}

    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.password = hash_password(user.password)
    db.commit()
    db.refresh(existing_user)
    return existing_user


@app.delete("/users/{user_id}")
# Anyone Can delete a user
# Because we are not checking for any authentication or authorization
# We need to Check
# 1.Who is calling this endpoint
# 2. What permissions do they have
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.id == user_id).first()
    if not existing_user:
        return {"error": "User not found"}

    db.delete(existing_user)
    db.commit()
    return {"message": "User deleted successfully"}



#JWT Authnticated API Example
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
@app.get("/profile")
def get_profile(
    token: str = Depends(oauth2_scheme)
):
    payload = verify_token(token)
    return {
        "message": "Protected profile data",
        "payload": payload
    }