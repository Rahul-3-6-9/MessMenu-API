from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse

from typing import List, Literal
import tempfile
import os

from fileReader import process_files
from models.schemas import ProcessMenuRequest, MenuResponse, ErrorResponse

router = APIRouter()

@router.post("/process")
async def process_menu(
    file_type: Literal["pdf", "excel", "gsheet"] = Form(..., description="Type of files to process"),
    files: List[UploadFile] = File(...)
):
    
    print(f"Received file_type: {file_type}")
    print(f"Received files: {[file.filename for file in files if file]}")

    try:
        with open("prompt.txt", "r") as f:
            prompt = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=ErrorResponse(error="prompt.txt not found").dict())

    temp_files = []
    try:
        if not files:
            raise HTTPException(status_code=422, detail=ErrorResponse(error="At least one file is required").dict())
        
        for file in files:
            if file_type == "pdf" and not file.filename.lower().endswith(".pdf"):
                raise HTTPException(status_code=422, detail=ErrorResponse(error=f"Invalid file: {file.filename}. Must be a PDF").dict())
            if file_type == "excel" and not file.filename.lower().endswith((".xlsx", ".xls")):
                raise HTTPException(status_code=422, detail=ErrorResponse(error=f"Invalid file: {file.filename}. Must be an Excel file (.xlsx or .xls)").dict())
            if file_type == "gsheet" and not file.filename.lower().endswith((".xlsx", ".xls")):
                raise HTTPException(status_code=422, detail=ErrorResponse(error=f"Invalid file: {file.filename}. Must be an Excel file (.xlsx or .xls) for gsheet").dict())
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type if file_type != 'gsheet' else 'xlsx'}") as temp_file:
                temp_file.write(await file.read())
                temp_files.append((file.filename, temp_file.name))
        
        result = process_files(temp_files, prompt)
        return JSONResponse(content=result, status_code=200)
    
    finally:
        for _, temp_path in temp_files:
            if os.path.exists(temp_path):
                os.unlink(temp_path)