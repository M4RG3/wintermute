import os
from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:

    working_dir_abs = os.path.abspath(working_directory)       
    abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_file_path: bool = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
    if not valid_file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    is_file: bool = os.path.isfile(abs_file_path)
    if not is_file:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
  
        with open(abs_file_path, "r") as f:
            file_content: str = f.read(MAX_CHARS)

            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content
    
    except Exception as e:
        return f'Error: {e}'