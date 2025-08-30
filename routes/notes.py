from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import List
from models.usermodel import TokenData
from models.notemodel import NotesContent,NotesContentResponse
from utils import oauth2
from config import db



router = APIRouter(
    tags=["Note Content"]
)

@router.post("/", response_description="Create Note Content", response_model=NotesContentResponse)
async def read_item(note_content: NotesContent, current_user=Depends(oauth2.get_current_user)):
    
    try:
     
        note_content = jsonable_encoder(note_content)
      
        note_content["last_update"] = datetime.now()
        note_content["created_on"] = datetime.now()
 
        new_note_content = await db["notes"].insert_one(note_content)

       
        created_note_post = await db["notes"].find_one({"_id": new_note_content.inserted_id})

        print(new_note_content.inserted_id)
        return created_note_post
    
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )



@router.get("/", response_description="Get Notes", response_model=List[NotesContentResponse])
async def get_notes(orderby: str = "created_on", current_user=Depends(oauth2.get_current_user)):
    try:
        Notes = await db["notes"].find({}, {"_id": 0}).sort(orderby, -1).to_list(length=None)
        print("datasend", Notes)  
        return Notes
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )



@router.delete("/{id}", response_description="Delete Note")
async def delete_note(id: str, current_user=Depends(oauth2.get_current_user)):
    note = await db["notes"].find_one({"note_id": id})

    if note:
        try:
            delete_result = await db["notes"].delete_one({"note_id": id})
            print("Delete count", delete_result.deleted_count)

            if delete_result.deleted_count == 1:
                return JSONResponse({"message": "Deleted successfully!"})

            raise HTTPException(status_code=404, detail=f"Note {id} not found")

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail="Internal server error"
            )
    else:
        raise HTTPException(status_code=404, detail=f"Note {id} not found")


@router.put("/{id}", response_description="Update Note Content")
async def update_note(id: str, note_data: NotesContent, current_user = Depends(oauth2.get_current_user)):

    note = await db["notes"].find_one({"note_id": id})

    if note:  
        try:
            updated_data = {
                "note_title": note_data.note_title,
                "note_content": note_data.note_content,
                "color": note_data.color,
                "last_update": datetime.now()
            }

            update_result = await db["notes"].update_one({"note_id": id}, {"$set": updated_data})
            print("Update count:", update_result.modified_count)

            if update_result.modified_count == 1: 
                updated_note = await db["notes"].find_one({"note_id": id})
                updated_note["_id"] = str(updated_note["_id"]) 
                updated_note["last_update"] = updated_note["last_update"].isoformat() 
                updated_note["created_on"] = updated_note["created_on"].isoformat() 
                print("updated_note", updated_note)
                return JSONResponse({"message": "Note updated successfully!", "note": updated_note})

            raise HTTPException(status_code=404, detail=f"Note {id} not found or no changes made")

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal server error")

    else: 
        raise HTTPException(status_code=404, detail=f"Note with ID {id} not found")