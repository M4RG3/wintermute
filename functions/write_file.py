import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
   
    working_dir_abs = os.path.abspath(working_directory)
    
    file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

    try:    
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        if not valid_target_dir:
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