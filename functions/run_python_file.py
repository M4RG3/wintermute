import os
import subprocess
from functions.get_safe_path import get_safe_path


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = get_safe_path(working_directory, file_path)

        if abs_file_path is None:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'


        is_file: bool = os.path.isfile(abs_file_path)
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        has_python_extension: bool = file_path.endswith(".py")
        if not has_python_extension:
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args is not None:
            command.extend(args)

        process_result = subprocess.run(args=command, 
                                        cwd=working_dir_abs, 
                                        capture_output=True,
                                        text=True,
                                        timeout=30)

        return_str: str = ""

        if process_result.returncode != 0:
            return_str += f"Process exited with code {process_result.returncode}\n"

        if process_result.stdout != "":
            return_str += f"STDOUT: {process_result.stdout}"

        if process_result.stderr !=  "":
            return_str += f"STDERR: {process_result.stderr}"

        if process_result.stderr ==  "" and process_result.stdout == "":
            return_str += "No output produced\n"    

        return return_str

    except Exception as e:
            return f'Error: executing Python file: {e}'
    