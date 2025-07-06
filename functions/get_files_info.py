import os
from google.genai import types

MAX_CHARS = 10000 
def get_files_info(working_directory, directory=None):
    try:
        directory = directory or "."
        full_path = os.path.abspath(os.path.join(working_directory, directory))
        base_path = os.path.abspath(working_directory)

        if not full_path.startswith(base_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        result = []
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            result.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(result)

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info=types.FunctionDeclaration(
    name="get_files_info",
    description="List files and directories in a specified directory within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files and directories from. Defaults to the current directory if not provided.",
                default=".",
            ),}
    )
)

