import os
from functions.get_file_content import get_file_content




def main():
    print("Result for file in 'main.py':")
    print(get_file_content("calculator", "main.py"))
    print("Result for file in 'pkg/calculator.py':")
    second = get_file_content("calculator", "pkg/calculator.py")
    print(second)   
    print("Result for file in '/bin/cat':")
    third = get_file_content("calculator", "/bin/cat")
    print(third)
    print("Result for file in 'pkg/does_not_exist.py':")
    fourth = get_file_content("calculator", "pkg/does_not_exist.py")
    print(fourth)

if __name__ == "__main__":
    main()