import os
import sys
from dotenv import load_dotenv
from google import genai 
from google.genai import types
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
   
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
avaliable_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,schema_get_file_content,
        schema_write_file,schema_run_python_file
    ]
)


def call_function(function_call_part, verbose=False):
    functions_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    working_directory = "./calculator"

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_to_call = functions_dict.get(function_call_part.name)

    if not function_to_call:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    args_with_working_dir = dict(function_call_part.args)
    args_with_working_dir["working_directory"] = working_directory
    function_result = function_to_call(**args_with_working_dir)


    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result}
            )
        ],
    )

system_prompt ="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt> [--verbose]")
        sys.exit(1)
    else:
        prompt = sys.argv[1]
        verbose = len(sys.argv) > 2 and sys.argv[2].lower() == '--verbose'

        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)]),
        ]
        for i in range(21):
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[avaliable_functions],
                    system_instruction=system_prompt
                ),
            )
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if response.function_calls:
                function_call_part = response.function_calls[0]
                function_result = call_function(function_call_part, verbose=verbose)

                messages.append(function_result)
            else:
                print(f"\nFinal response:\n{response.text}")
                break



if __name__ == "__main__":
    main()