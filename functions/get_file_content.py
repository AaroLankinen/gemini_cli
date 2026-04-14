import os
from config import MAX_CHARS



def get_file_content(working_directory, file_path):
    try:
        if not os.path.isdir(working_directory):
            raise Exception(f'"{working_directory}" is not a directory')
        target_dir = os.path.normpath(os.path.join(working_directory, file_path))
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(target_dir)]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            raise Exception(f'Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(f"{working_directory}/{file_path}"):
            raise Exception(f'File not found or is not a regular file: "{file_path}"')
        content = open(f"{working_directory}/{file_path}", "r").read(MAX_CHARS)
        if len(content) == MAX_CHARS:
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content


    except Exception as e:
        return f"Error: {e}"