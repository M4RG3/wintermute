import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function
import json

def main():

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    
    if api_key == None:
        raise RuntimeError("unable to resolve api key")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args.verbose, args.user_prompt)


def generate_content(client: OpenAI, messages: list, is_verbose: bool, user_prompt: str) -> None:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    print("Response:")
    
    message = response.choices[0].message
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, is_verbose)
            if not result_message["content"]:
                raise Exception(f"Error: Function {tool_call.function.name} returned no content.")
            if is_verbose:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
if __name__ == "__main__":
    main()
