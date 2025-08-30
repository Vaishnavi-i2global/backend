from pydantic_core import core_schema
from pydantic import BaseModel,Field,EmailStr
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import uuid


class NotesContent(BaseModel):
    note_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    note_title:str= Field(...)
    note_content:str= Field(...)
    color:str= Field(...)
    last_update: datetime = datetime.now()
    created_on:  datetime = datetime.now()
    class config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        json_schema_extra = {
            "example":{
                "note_id": "rtsbbbg7-1edf-4333-97c9-f6a654021eea0",
                "note_title":"Note Title",
                "note_content":"Note Content",
                "color":"red",
                "last_update": "2024-11-10T00:00:00",
                "created_on": "2024-11-10T00:00:00"
            }
        }


class NotesContentResponse(BaseModel):
    note_id:str = Field(...)
    note_title: str = Field(...)
    color: str = Field(...)
    note_content: str = Field(...)
    created_on: datetime = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}
        json_schema_extra = {
            "example": {
                "note_title": "note title",
                "note_content": "note content",
                "color": "note color",
                "created_at": "Date of note creation"
            }
        }
