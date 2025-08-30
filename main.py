from fastapi import FastAPI
from routes import users
from routes import notes
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost:3000",  
    "http://localhost:8000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["*"],  
)



app.include_router(users.router,prefix="/api/users")
app.include_router(notes.router,prefix="/api/notes")