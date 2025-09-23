import os

def addition(a: float, b: float) -> float:
    """
    Return the sum of two floats.

    Args:
        a (float): The first float.
        b (float): The second float.
    Returns:
        float: The sum of a and b.
    """
    return a + b

def subtraction(a: float, b: float) -> float:
    """
    Return the difference between two floats.

    Args:
        a (float): The float to subtract from.
        b (float): The float to subtract.
    Returns:
        float: The result of a minus b.
    """
    return a - b

def multiplication(a: float, b: float) -> float:
    """
    Return the product of two floats.

    Args:
        a (float): The first float.
        b (float): The second float.
    Returns:
        float: The product of a and b.
    """
    return a * b

def division(a: float, b: float) -> float:
    """
    Return the quotient of two floats as a float.

    Args:
        a (float): The dividend.
        b (float): The divisor (must not be zero).
    Returns:
        float: The result of a divided by b.
    Raises:
        ZeroDivisionError: If b is zero.
    """
    return a / b

def read_file(file_path: str) -> str:
    with open(file_path, "r") as f:
        text = f.read()
    return text[:10000]

def read_images(image_paths: list[str]) -> list[str]:
    return [read_file(image_path) for image_path in image_paths]

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
    
