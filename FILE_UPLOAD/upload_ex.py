from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os

app = FastAPI()


# Create uploads folder if not exists
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):
    # Validate file type
    allowed_types = [
        "image/jpeg",
        "image/png",
        "application/pdf"
    ]
    
    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail="Invalid file type"
        )
        
    file_path = f"{UPLOAD_FOLDER}/{file.filename}"
    
    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )
        
    return {
        "message": "File uploaded successfully",
        "file_name": file.filename,
        "content_type": file.content_type,
        "saved_path": file_path
    }