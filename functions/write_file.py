import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    base_path = os.path.abspath(working_directory)
    
    if not full_path.startswith(base_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" {(content)} '
    except Exception as e:
        return f"Error: {str(e)}"

schema_write_file=types.FunctionDeclaration(
    name="write_file",
    description="Write content to a file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties=
    {
        "file_path":types.Schema(
            type=types.Type.STRING,
            description="The path to the file where content will be written, relative to the working directory.",

        ),
        "content":types.Schema(
            type=types.Type.STRING,
            description="The content to write to the file."
        ) ,}
    )
)