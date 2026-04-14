import os
import subprocess
from config import MAX_CHARS



def run_python_file(working_directory, file_path, args=None):
    try:
        if not os.path.isdir(working_directory):
            raise Exception(f'"{working_directory}" is not a directory')
        target_dir = os.path.normpath(os.path.join(working_directory, file_path))
        valid_target_dir = os.path.commonpath([os.path.abspath(working_directory), os.path.abspath(target_dir)]) == os.path.abspath(working_directory)
        if not valid_target_dir:
            raise Exception(f'Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(f"{working_directory}/{file_path}"):
            raise Exception(f'"{file_path}" does not exist or is not a regular file')
        if not file_path.endswith(".py"):
            raise Exception(f'"{file_path}" is not a Python file')

        result = subprocess.run(["python3", f"{working_directory}/{file_path}"] + (args or []), capture_output=True, text=True, timeout=30)
        output = ""
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        elif not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            output += f"STDOUT: {result.stdout}STDERR: {result.stderr}\n"
        return output[:MAX_CHARS] + (f'[...Output truncated at {MAX_CHARS} characters]' if len(output) > MAX_CHARS else "")
    except Exception as e:
        return f"Error: executing Python file: {e}"