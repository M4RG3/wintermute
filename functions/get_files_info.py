import os
from functions.get_safe_path import get_safe_path

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_dir = get_safe_path(working_directory, directory)

        if target_dir is None:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        files = os.listdir(target_dir)
        file_descriptions: list[str] = []
        for file in files:
            file_path = os.path.join(target_dir, file)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_descriptions.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(file_descriptions)
    
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}   