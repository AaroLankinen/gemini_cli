import os

from functions.get_files_info import get_files_info






def main():
    print("Result for current directory:")
    first = get_files_info("calculator", ".")
    print(first)
    print("Result for 'pkg' directory:")
    second = get_files_info("calculator", "pkg")
    print(second)
    print("Result for '/bin' directory:")
    third = get_files_info("calculator", "bin")
    print(third)
    print("Result for '../' directory:")
    fourth = get_files_info("calculator", "../")
    print(fourth)


if __name__ == "__main__":
    main()