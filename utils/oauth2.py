from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from typing import Dict
from models.usermodel import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from config import db
import os
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES =int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',30))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")



def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    print("**To Encode",to_encode)
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration_time})

    jw_token = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return jw_token

def verify_access_token(token: str, credential_exception: Dict):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Payload****^^^^@@@@@",payload)

        name: str = payload.get("sub")

        if not name:
            raise credential_exception

        token_data = TokenData(name=name)
        print("!!!!!!TOKEN DATA *****",token_data.name)
        return token_data
    except JWTError:
        raise credential_exception
   

async def get_current_user(token: str = Depends(oauth2_scheme)):
    print("tokennnnnn ",token)
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify token, token expired",
        headers={"WWW-AUTHENTICATE": "Bearer", }
    )

    current_user_name = verify_access_token(
        token=token, credential_exception=credential_exception).name
    print("&&&&CURRENT USER NAME",current_user_name)
    current_user = await db["users"].find_one({"name": current_user_name})
    print("&&&&CURRENT USER  &&&&",current_user)

    return current_user