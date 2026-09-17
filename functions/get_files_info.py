import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        
        valid_target_dir: bool = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        valid_directory: bool = os.path.isdir(target_dir)
        if not valid_directory:
            return f'Error: "{directory}" is not a directory'

        
        files = os.listdir(target_dir)
        file_descriptions: list = []
        for file in files:
            file_path = os.path.join(target_dir, file)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            file_descriptions.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(file_descriptions)
    
    except Exception as e:
        return f"Error: {e}"

    