from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import SessionLocal

from models.user import Users

from schemas.user import UserCreate, UserLogin

from services.auth_service import hash_password, verify_password, create_access_token

from utils.dependencies import get_current_user, admin_only

router = APIRouter()

# =========================
# DB Dependency
# =========================


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# GET USERS
# =========================


@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(Users).all()

    return users


# =========================
# CREATE USER
# =========================


@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = Users(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# =========================
# LOGIN API
# =========================


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(Users).filter(Users.email == user.email).first()

    if not db_user:

        raise HTTPException(status_code=400, detail="User not found")

    verified = verify_password(user.password, db_user.password)

    if not verified:

        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = create_access_token(
        {"user_id": db_user.id, "email": db_user.email, "role": db_user.role}
    )

    return {"access_token": access_token, "token_type": "bearer"}


# =========================
# PROTECTED API
# =========================


@router.get("/profile")
def get_profile(current_user=Depends(get_current_user)):

    return {"message": "Protected profile data", "user": current_user}


# =========================
# ADMIN ONLY API
# =========================


@router.get("/admin")
def admin_dashboard(current_user=Depends(admin_only)):

    return {"message": "Welcome Admin 🚀", "user": current_user}
