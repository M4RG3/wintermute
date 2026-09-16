import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

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
        {"role": "user", "content": args.user_prompt},
        ]
    generate_content(client, messages, args.verbose, args.user_prompt)


def generate_content(client: OpenAI, messages: list, is_verbose: bool, user_prompt: str) -> None:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
