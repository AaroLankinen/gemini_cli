import os




'''
This function retrieves information about files in a specified directory, ensuring that the directory is within a permitted working directory. 
It returns a formatted string containing the file name, size, and whether it is a directory. 
If any errors occur (e.g., invalid directories), it returns an error message.
'''
def get_files_info(working_directory, directory="."):
    try:
        if not os.path.isdir(working_directory):
            raise Exception(f'"{working_directory}" is not a directory')

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if not os.path.isdir(target_dir):
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')

        files_info = ""
        for file in os.listdir(target_dir):
            is_directory = os.path.isdir(os.path.join(target_dir, file))
            file_name, file_extension = os.path.splitext(file)
            file_path = os.path.join(target_dir, file)
            relative_path = os.path.relpath(file_path, working_directory)
            file_size = os.path.getsize(file_path)
            files_info += f"- {file_name}{file_extension}: file_size = {file_size} bytes, is_dir={is_directory}\n"

        return files_info
    except Exception as e:
        return f"Error: {e}"




def main():
    working_directory = os.getcwd()
    directory = "."
    print(get_files_info(working_directory, directory))

if __name__ == "__main__":
    main()