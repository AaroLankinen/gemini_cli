import os
from config import MAX_CHARS




def write_file(working_directory, file_path, content):
    try:
        if not os.path.isdir(working_directory):
            raise Exception(f'"{working_directory}" is not a directory')
        target_dir = os.path.normpath(os.path.join(working_directory, file_path))
        if target_dir.endswith("/"):
            raise Exception(f'Cannot write to "{file_path}" as it is a directory')
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(target_dir)]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            raise Exception(f'Cannot write to "{file_path}" as it is outside the permitted working directory')
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(f"{working_directory}/{file_path}", "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"