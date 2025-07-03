import os
import sys
from dotenv import load_dotenv
from google import genai 
from google.genai import types
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():
       if len(sys.argv) < 2:
           print("Usage: python main.py <your_api_key>")
           sys.exit(1)
       else:
        prompt = sys.argv[1]
        
        verbose = len(sys.argv) > 2 and sys.argv[2].lower() == '--verbose'
                 
        messages=[
    types.Content(role="user",parts=[types.Part(text=prompt)]),
]

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
        model='gemini-2.0-flash-001',contents=messages
    )

        print(response.text)
        
        if verbose:
            print(f"User prompt: {prompt} \nPrompt tokens: {response.usage_metadata.prompt_token_count} \nResponse tokens: {response.usage_metadata.candidates_token_count} \n")

if __name__ == "__main__":
    main()