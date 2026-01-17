# C:\Users\Pranav\Downloads\document-processor\app\main.py

import os
import tempfile
import traceback
import uvicorn
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from core.task_processor import TaskProcessor

# Initialize the FastAPI app
app = FastAPI(
    title="Scalable Document Processor",
    description="An expert-level API to process large documents with AI."
)

# Initialize our main processor once at startup for efficiency
processor = TaskProcessor()

@app.on_event("startup")
async def startup_event():
    # Read host and port from environment variables, with sensible defaults
    # This makes the startup message flexible and configurable
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    
    # Use 127.0.0.1 for the clickable link if host is 0.0.0.0
    clickable_host = "127.0.0.1" if host == "0.0.0.0" else host
    docs_url = f"http://{clickable_host}:{port}/docs"
    
    print("\n=====================================================================")
    print("🚀 Your AI Document Processor is running!")
    print("Access the API documentation (Swagger UI) here:")
    # The \033[1m and \033[0m are ANSI codes to make the link bold in most terminals
    print(f"👉 \033[1m{docs_url}\033[0m 👈 (CTRL + Click to open)")
    print("=====================================================================\n")
# -------------------------------------


def safe_delete(path: str):
    """A robust function to delete a file, ignoring errors if it's already gone."""
    try:
        if os.path.exists(path):
            os.unlink(path)
            print(f"[INFO] Cleaned up temporary file: {path}")
    except Exception as e:
        print(f"[ERROR] Could not clean up file {path}. Reason: {e}")

@app.post("/process-document/")
async def process_document_endpoint(
    background_tasks: BackgroundTasks,
    task_instruction: str = Form(..., description="The specific task to perform (e.g., 'Summarize this document')."),
    file: UploadFile = File(...)
):
    """
    The main endpoint to upload a .docx file and process it.
    """
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .docx file.")

    print(f"[INFO] ==> Step 1: Request received for task '{task_instruction}'. File: '{file.filename}'.")
    
    uploaded_file_path = None
    try:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_upload:
            uploaded_file_path = tmp_upload.name
            tmp_upload.write(await file.read())
            print(f"[INFO]     - Uploaded file saved to temporary path: {uploaded_file_path}")

        # Call the core processor to handle the entire workflow
        result_file_path = processor.process_task(
            file_path=uploaded_file_path,
            task_instruction=task_instruction,
            original_filename=file.filename
        )
        
        # Schedule the temporary files to be deleted after the response is sent
        background_tasks.add_task(safe_delete, uploaded_file_path)
        background_tasks.add_task(safe_delete, result_file_path)
        
        print(f"[INFO] ==> Step 4b: Task complete. Sending response to client.")
        
        return FileResponse(
            path=result_file_path,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=f"result_{file.filename}"
        )
        
    except Exception as e:
        # If anything goes wrong, log the error and clean up the uploaded file
        traceback.print_exc()
        if uploaded_file_path:
            background_tasks.add_task(safe_delete, uploaded_file_path)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {str(e)}")

if __name__ == "__main__":
    # This allows running the app directly for development
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)