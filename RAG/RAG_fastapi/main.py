from fastapi import (
    BackgroundTasks,
    FastAPI, 
    HTTPException,
    status, 
    File, 
    UploadFile, Depends, Request, Body
    )
from typing import Annotated
from rag_process import pdf_text_extractor, vector_service
from .upload import save_file
from .models import generate_text
from .schemas import TextModelRequest, TextModelResponse

app = FastAPI()

@app.post("/upload")
async def file_upload_controller(
    file: Annotated[UploadFile, File(description="Uploaded PDF documents")],
    bg_text_processor: BackgroundTasks,
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            detail=f"Only uploading PDF documents are supported",
             status_code=status.HTTP_400_BAD_REQUEST,
        )
    try:
        filepath = await save_file(file)
        bg_text_processor.add_task(pdf_text_extractor, filepath)
        bg_text_processor.add_task(
            vector_service.store_file_content_in_db,
            filepath.replace("pdf", "txt"),
            512,
            "knowledgebase",
            768,
        )
    except Exception as e:
        raise HTTPException(
            detail=f"An error occurred while saving file - Error: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.post("/generate/text", response_model_exclude_defaults=True)
async def serve_text_to_text_controller(
    request: Request,
    body: TextModelRequest = Body(...),
    urls_content: str = Depends(get_urls_content),
    rag_content: str = Depends(get_rag_content),
) -> TextModelResponse:
    ...  # Raise HTTPException for invalid models
    prompt = body.prompt + " " + urls_content + rag_content
    output = await generate_text(body.prompt, body.temperature)
    return TextModelResponse(content=output, ip=request.client.host)