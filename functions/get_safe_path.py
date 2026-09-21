import os

def get_safe_path(working_directory, file_path):
    absolute_working_dir = os.path.abspath(working_directory)
    absolute_file_path = os.path.abspath(
        os.path.join(working_directory, file_path)
    )

    if os.path.commonpath([absolute_working_dir, absolute_file_path]) != absolute_working_dir:
        return None

    return absolute_file_path