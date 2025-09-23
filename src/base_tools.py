import os
import math

### Math tools ###

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


def exponentiation(a: float, b: float) -> float:
    """
    Return the result of raising a to the power of b.

    Args:
        a (float): The base.
        b (float): The exponent.
    Returns:
        float: The result of a ** b.
    """
    return math.pow(a, b)

def square_root(a: float) -> float:
    """
    Return the square root of a float.

    Args:
        a (float): The number to find the square root of.
    Returns:
        float: The square root of a.
    """
    return math.sqrt(a)

def sine(x: float) -> float:
    """
    Return the sine of x (in radians).

    Args:
        x (float): The angle in radians.
    Returns:
        float: The sine of x.
    """
    return math.sin(x)

def cosine(x: float) -> float:
    """
    Return the cosine of x (in radians).

    Args:
        x (float): The angle in radians.
    Returns:
        float: The cosine of x.
    """
    return math.cos(x)

def tangent(x: float) -> float:
    """
    Return the tangent of x (in radians).

    Args:
        x (float): The angle in radians.
    Returns:
        float: The tangent of x.
    """
    return math.tan(x)

def logarithm(a: float, base: float = math.e) -> float:
    """
    Return the logarithm of a with the specified base.

    Args:
        a (float): The number to take the logarithm of.
        base (float, optional): The logarithmic base. Defaults to math.e (natural logarithm).
    Returns:
        float: The logarithm of a to the given base.
    """
    return math.log(a, base)

def absolute_value(a: float) -> float:
    """
    Return the absolute value of a float.

    Args:
        a (float): The number to get the absolute value of.
    Returns:
        float: The absolute value of a.
    """
    return abs(a)




### File tools ###

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

### Python interpreter tools ###

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
    
