import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.run_python_file import run_python_file
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info

from functions.call_function import available_functions
from functions.call_function import call_function

from prompts import system_prompt

from config import MAX_ITERATIONS



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

# Initialize messages with the user prompt
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]



for iteration in range(MAX_ITERATIONS):  # Limit the number of iterations to prevent infinite loops
    # Generate content using the specified model
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            max_output_tokens=2048,
        )
    )

    # Check if the response contains candidates and append their content to messages
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)
            else:
                raise RuntimeError("Candidate content is None.")
    else:
        raise RuntimeError("No candidates found in response.")

    # Process the response and handle function calls
    if response.usage_metadata is not None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"Total tokens: {response.usage_metadata.total_token_count}")
        if response.function_calls:
            function_call_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                messages.append(function_call_result)
                if function_call_result.parts[0].function_response == None:
                    raise RuntimeError(f"Function {function_call.name} returned no response.")
                if function_call_result.parts[0].function_response.response == None:
                    raise RuntimeError(f"Function {function_call.name} returned an empty response.")
                function_call_results.append(function_call_result)
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print("Response:", response.text)
            break
    else:
        raise RuntimeError("Usage metadata not found in response, likely failed API call.")

    # Check if the maximum number of iterations has been reached to prevent infinite loops
    if iteration == MAX_ITERATIONS - 1:
        print("Maximum iterations reached. Stopping to prevent infinite loop.")
        exit(1)
    
