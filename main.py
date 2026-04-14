import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from prompts import system_prompt



# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Gemini CLI")
parser.add_argument("user_prompt", type=str, help="The user prompt for content generation.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Create content request with the user prompt
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

# Generate content using the specified model
response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        max_output_tokens=2048,
    )
)
if response.usage_metadata is not None:
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(f"Total tokens: {response.usage_metadata.total_token_count}")
    print("Response:", response.text)
else:
    raise RuntimeError("Usage metadata not found in response, likely failed API call.")
