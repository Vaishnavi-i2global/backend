from fastapi import APIRouter, HTTPException, status, Depends
from models.usermodel import User, UserResponse, TokenData, UserLogin, UserLoginResponse
from fastapi.security import OAuth2PasswordRequestForm
from utils.utils import get_password_hash,verify_password
from fastapi.encoders import jsonable_encoder
from config import db
from utils import oauth2
import secrets
from datetime import datetime


router= APIRouter(
    tags=["Users Route"]
)

@router.post("/register",response_description="Register a new user",response_model=UserResponse)
async def registration(user_info:User):
    user_info = jsonable_encoder(user_info)
    user_found = await db["users"].find_one({"user_name":user_info["user_name"]})
    email_found = await db["users"].find_one({"user_email":user_info["user_email"]})
     
    if user_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="UserName already taken")

    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already exists")

    #Hashing
    print(user_info["password"],"Password")
    user_info["password"] = get_password_hash(user_info["password"])
    user_info["create_on"] = datetime.now()
    user_info["last_update"] = datetime.now()

    #api key 
    # user_info["apiKey"]= secrets.token_hex(30)

    new_user = await db["users"].insert_one(user_info)
    created_user = await db["users"].find_one({"_id":new_user.inserted_id})

    return created_user



@router.post("/login", response_description="Login user", response_model=UserLoginResponse)
async def login(user_login: UserLogin):
    # Check if user exists
    user = await db["users"].find_one({"user_email": user_login.user_email})
    
    if user and verify_password(user_login.password, user["password"]):
        access_token = oauth2.create_access_token(
            data={"sub": user["user_name"]}
        )
        return {"access_token": access_token, "user_name": user["user_name"]}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid user credentials"
        )