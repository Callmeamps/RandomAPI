from fastapi import APIRouter

from data.user_utils import get_current_user, sign_up, sign_in_w_password, sign_out

router = APIRouter()

current_user = get_current_user()

@router.post("/signup")
def register(email: str, password: str, username: str):
    return sign_up(email, password, username)

@router.post("/signin")
def sign_in(email: str, password: str):
    return sign_in_w_password(email, password)

@router.post("/signout")
def signout():
    return sign_out()
