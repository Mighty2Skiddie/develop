import os
import tempfile
from docx import Document

def create_docx_from_text(text: str, original_filename: str) -> str:
    """
    Creates a new .docx document from a string of text.

    Args:
        text: The final text content to be written to the document.
        original_filename: The name of the original file, used for naming the result.

    Returns:
        The file path of the newly created .docx document.
    """
    print(f"[INFO] ==> Step 4a: Final result compiled. Creating output document...")

    # Create a new blank Word document
    doc = Document()
    
    # Split the result text by newlines and add each part as a paragraph
    # This preserves the paragraph structure of the AI's output.
    for paragraph in text.split('\n'):
        doc.add_paragraph(paragraph)

    # Save the document to a temporary file with a descriptive name
    # The 'delete=False' flag is crucial because it allows us to use the file path
    # after the 'with' block closes. The file will be deleted later by our API.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx", prefix=f"result_{os.path.splitext(original_filename)[0]}_") as tmp:
        output_path = tmp.name
        doc.save(output_path)
        print(f"[INFO]     - Output document saved to temporary path: {output_path}")

    return output_path
