from fastapi import Depends, HTTPException

from fastapi.security import OAuth2PasswordBearer

from services.auth_service import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# =========================
# GET CURRENT USER
# =========================


def get_current_user(token: str = Depends(oauth2_scheme)):

    payload = verify_token(token)

    return payload


# =========================
# ADMIN ONLY DEPENDENCY
# =========================


def admin_only(current_user=Depends(get_current_user)):

    if current_user.get("role") != "admin":

        raise HTTPException(status_code=403, detail="Admin access required")

    return current_user
