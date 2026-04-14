import os
from functions.write_file import write_file



def main():
    print("Testing write_file function:")
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result1)
    result3 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result3)
    result4 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result4)

if __name__ == "__main__":
    main()