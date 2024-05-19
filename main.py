from P2J import empty_files
from P2J import write_files
from P2J import read_files
from P2J import if_stmnt




def main():
    input_file = 'input.txt'
    output_file = 'output.txt'
    python_if_statement = """if x > 10:
    print("x is greater than 10")
    print("hey")
    else:
    print("x is less than or equal to 10")
    print("hi")
    """
    empty_files(output_file)
    empty_files(input_file)

    write_files(python_if_statement , input_file)

    content = read_files(input_file)

    translation = if_stmnt(content)
    print(translation)

    write_files(translation , output_file)
if __name__ == "__main__":
    main()