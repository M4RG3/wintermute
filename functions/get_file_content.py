import os
from config import MAX_CHARS
from functions.get_safe_path import get_safe_path


def get_file_content(working_directory: str, file_path: str) -> str:

    try:

        abs_file_path = get_safe_path(working_directory, file_path)
        
        if abs_file_path is None:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        is_file: bool = os.path.isfile(abs_file_path)
  
        with open(abs_file_path, "r") as f:
            file_content: str = f.read(MAX_CHARS)

            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content
    
    except Exception as e:
        return f'Error: {e}'


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the content of a specified file relative to the working directory, limited to a maximum number of characters",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to retrieve content from, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}   