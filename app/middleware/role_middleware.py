from fastapi import HTTPException

def require_role(user, role):
    if user.get("role") != role:
        raise HTTPException(403, "Access Denied")