import os
from google.genai import types
MAX_CHARS = 10000  
def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    base_path = os.path.abspath(working_directory)
    if not full_path.startswith(base_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory' 
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read(MAX_CHARS)
        if len(content) == MAX_CHARS:
            content += f'\n...File "{file_path}" truncated at {MAX_CHARS} characters...'
        return content
    except Exception as e:
        return f"Error: {str(e)}"
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieve the content of a file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        }
    )
)