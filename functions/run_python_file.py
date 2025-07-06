import os
import subprocess
from google.genai import types
def run_python_file(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    base_path = os.path.abspath(working_directory)

    if not full_path.startswith(base_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'

    if not full_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    try:    
        result = subprocess.run(
            ['python', full_path],
            capture_output=True,
            text=True,
            cwd=working_directory,
            timeout=30,
            
            )
        output_lines = []

        if result.stdout:
            output_lines.append("STDOUT:\n" + result.stdout.strip())
        if result.stderr:
            output_lines.append("STDERR:\n" + result.stderr.strip())

        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        return "\n".join(output_lines) or f"File {file_path} - No output produced."
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Run a Python file in the specified working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
            }
        )
    )   
    
    