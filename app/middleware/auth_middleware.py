from fastapi import Header, HTTPException
from app.utils.jwt_handler import verify_token

def get_current_user(token: str = Header()):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(401, "Invalid Token")
    return payload