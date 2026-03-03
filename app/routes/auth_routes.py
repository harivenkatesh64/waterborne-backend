from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from app.database import users_collection
from app.schemas.user_schema import UserRegister, UserLogin
from app.utils.dependencies import get_current_user
from app.utils.password_handler import hash_password, verify_password
from app.utils.jwt_handler import create_token
from app.models.user_model import UserModel
from app.logger import logger

router = APIRouter()

# 🔹 Change Password Model
class ChangePasswordModel(BaseModel):
    old_password: str
    new_password: str


# 🔹 Register User
@router.post("/register")
def register(user: UserRegister):

    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer"
        )

    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    user_doc = UserModel.create_user_document(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    users_collection.insert_one(user_doc)

    return {"message": "User registered successfully"}

# 🔹 Login User
@router.post("/login")
def login(user: UserLogin):

    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "email": db_user["email"],
        "role": db_user["role"]
    })

    logger.info(f"User logged in: {user.email}")

    return {"access_token": token}


# 🔹 Get Current Logged-In User (For Frontend Redirect)
@router.get("/me")
def get_current_user_details(current_user=Depends(get_current_user)):
    return current_user


# 🔹 Change Password Endpoint
@router.put("/change-password")
def change_password(
    data: ChangePasswordModel,
    current_user=Depends(get_current_user)
):

    db_user = users_collection.find_one({"email": current_user["email"]})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Verify old password
    if not verify_password(data.old_password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    # ✅ Hash new password
    new_hashed_password = hash_password(data.new_password)

    # ✅ Update password in database
    users_collection.update_one(
        {"email": current_user["email"]},
        {"$set": {"password": new_hashed_password}}
    )

    logger.info(f"Password changed for user: {current_user['email']}")

    return {"message": "Password changed successfully"}