import os

def read_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        text = f.read()
    return text[:10000]

def write_file(file_path: str, text: str) -> None:
    with open(file_path, "w") as f:
        try:
            f.write(text)
            return f"File written successfully to {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"

def list_files(directory: str) -> list[str]:
    return os.listdir(directory)

def python_eval(code: str) -> str:
    try:
        result = eval(code)
        return str(result)
    except Exception as e:
        return f"Error evaluating code: {e}"


if __name__ == "__main__":

    print(python_eval("1 + 1"))

    write_file("test.txt", "Hello, world!")

    print(read_file("test.txt"))
    
