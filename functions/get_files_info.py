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

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            raise Exception(f'Cannot list "{directory}" as it is outside the permitted working directory')

        files_info = ""
        try:
            for file_name_only in os.listdir(target_dir):
                file_path_abs = os.path.join(target_dir, file_name_only)
                
                is_directory = os.path.isdir(file_path_abs)
                
                file_size_str = "N/A" # Default for cases where size cannot be determined
                try:
                    file_size = os.path.getsize(file_path_abs)
                    file_size_str = f"{file_size} bytes"
                except FileNotFoundError:
                    file_size_str = "N/A (file not found)"
                except PermissionError:
                    file_size_str = "N/A (permission denied)"
                
                files_info += f"- {file_name_only}: file_size={file_size_str}, is_dir={is_directory}\n"
        except FileNotFoundError:
            return f'Error: Directory not found: "{directory}"'
        except NotADirectoryError:
            return f'Error: Path is not a directory: "{directory}"'
        except PermissionError:
            return f'Error: Permission denied to list directory: "{directory}"'
        except OSError as e:
            return f'Error: An OS error occurred while accessing "{directory}": {e}'

        return files_info
    except Exception as e:
        return f"Error: {e}"






def main():
    working_directory = os.getcwd()
    directory = "."
    print(get_files_info(working_directory, directory))

if __name__ == "__main__":
    main()