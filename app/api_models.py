# C:\Users\Pranav\Downloads\document-processor\app\api_models.py

from pydantic import BaseModel

class TaskResponse(BaseModel):
    """
    A Pydantic model to define the structure of a successful task response.
    This is not used for the file download but could be used for other endpoints.
    """
    message: str
    task: str
    input_file: str
    output_file: str

class ErrorResponse(BaseModel):
    """
    A Pydantic model for returning structured error messages.
    """
    detail: str