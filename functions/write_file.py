import os
from functions.get_safe_path import get_safe_path


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:    
        
        file_path_abs = get_safe_path(working_directory, file_path)

        if file_path_abs is None:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        valid_directory: bool = os.path.isdir(file_path_abs)
        if valid_directory:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(file_path_abs)
        os.makedirs(parent_dir, exist_ok=True)

        with open(file_path_abs, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write content to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                }
            },
            "required": ["file_path", "content"],
        },
    },
}   