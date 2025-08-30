from pydantic_core import core_schema
from pydantic import BaseModel,Field,EmailStr
from bson import ObjectId
import uuid
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class User(BaseModel) :
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_name: str = Field(...)
    user_email: EmailStr =  Field(...)
    password : str = Field(...)
    last_update: datetime = datetime.now()
    create_on:  datetime = datetime.now()

    class config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        json_schema_extra = {
            "example":{
                "user_id": "b8abbbf7-0d8f-4333-97c9-f6a93021eea0", 
                "user_name": "Vaishnavi",
                "user_email": "vaishu@gmail.com",
                "password": "secret_pass",
                "last_update": "2024-11-10T00:00:00",
                "create_on": "2024-11-10T00:00:00"
            }
        }

        
class UserResponse(BaseModel) :

    user_id: str = Field(...)
    user_name: str = Field(...)
    user_email: EmailStr =  Field(...)

    class config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        json_schema_extra = {
            "example":{
                "name":"Vaishnavi",
                "email":"vaishu@gmail.com",

            }
        }


class TokenData(BaseModel):
    name:str



class UserLogin(BaseModel) :

    
    user_email: EmailStr =  Field(...)
    password : str = Field(...)

    class config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        json_schema_extra = {
            "example":{
                "user_email":"vaishu@gmail.com",
                "password":"sceret_pass"
            }
        }

class UserLoginResponse(BaseModel):
    access_token: str
    user_name: str

    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJBa2lsYW4iLCJleHAiOjE3MzEzNDMxMDV9.Y2jpZn2kV3JS137-rDlnKaAEkdZ4kfF3wqLzoWaziH4",
                "user_name": "Vaishnavi",
            }
        }