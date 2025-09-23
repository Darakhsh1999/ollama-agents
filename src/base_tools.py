import os
import math
import ast
import io
import sys
import signal
import contextlib

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

def _assert_safe_imports(code: str, *, allowed: set[str] | None, denied: set[str]) -> None:
    """
    Parse code and ensure that import statements only import from the allowed set
    and never from the denied set. If allowed is None, disallow all imports except
    standard safe defaults (none by default). Raises ValueError on violation.
    """
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as e:
        # Let the runner handle syntax errors; only gate on imports here
        return

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            else:  # ast.ImportFrom
                base = (node.module or "").split(".")[0]
                names = [base] if base else []

            for mod in names:
                if mod in denied:
                    raise ValueError(f"Import of module '{mod}' is denied for safety.")
                # If no allowlist is provided, disallow all imports
                if allowed is None:
                    raise ValueError("Imports are not allowed in this sandbox.")
                if mod not in allowed:
                    raise ValueError(f"Import of module '{mod}' is not in the allowed list.")


def python_run(
    code: str,
    *,
    allowed_imports: list[str] | None = None,
    denied_imports: list[str] | None = None,
    timeout_seconds: int = 2,
) -> str:
    """
    Execute a Python code snippet in a constrained environment.

    Behavior:
    - Blocks dangerous imports and builtins. You may optionally pass an allowlist of importable modules.
    - Captures stdout and stderr. If code is a single expression, returns its value; otherwise, returns captured output.
    - Enforces a CPU-time timeout using signal.alarm on Unix systems.

    Args:
        code: The Python code to run. If it is a single expression, its value is returned.
        allowed_imports: If provided, only these top-level modules may be imported (e.g., ["math", "json"]).
        denied_imports: These modules are explicitly denied regardless of allowlist.
        timeout_seconds: Max seconds to run before timing out.

    Returns:
        str: The result of the expression or the captured stdout. Errors are returned as strings prefixed with 'Error:'.
    """

    # Default-deny list of sensitive modules
    default_denied = {
        "os",
        "sys",
        "subprocess",
        "shutil",
        "socket",
        "pathlib",
        "importlib",
        "ctypes",
        "multiprocessing",
        "threading",
        "resource",
        "signal",
        "selectors",
        "ssl",
        "http",
        "urllib",
        "ftplib",
        "telnetlib",
        "xml",
        "builtins",  # prevent tinkering
    }
    denied = default_denied | set(denied_imports or [])
    allowed = set(allowed_imports) if allowed_imports is not None else None

    # Validate imports statically
    try:
        _assert_safe_imports(code, allowed=allowed, denied=denied)
    except Exception as e:
        return f"Error: {e}"

    # Prepare a restricted set of builtins
    safe_builtins = {
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
        "range": range,
        "len": len,
        "enumerate": enumerate,
        "round": round,
        "sorted": sorted,
        "map": map,
        "filter": filter,
        "any": any,
        "all": all,
        "bool": bool,
        "int": int,
        "float": float,
        "str": str,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "zip": zip,
        # NOTE: Do not expose __import__ to block dynamic imports
    }

    # Pre-inject commonly safe modules (read-only references)
    preloaded_modules = {
        "math": math,
    }

    # If an allowlist is provided, pre-import those modules if they are safe and not denied
    if allowed is not None:
        for modname in allowed:
            if modname in denied:
                return f"Error: Import of module '{modname}' is denied for safety."
            # Only allow a narrow set of standard-library utilities by default
            if modname in ("math", "cmath", "statistics", "random", "re", "json"):
                try:
                    preloaded_modules[modname] = __import__(modname)
                except Exception:
                    return f"Error: Failed to import allowed module '{modname}'."
            else:
                # Disallow importing arbitrary modules even if listed, unless handled above
                return f"Error: Module '{modname}' is not approved for import in this sandbox."

    # Build execution globals with restricted builtins and preloaded modules
    exec_globals = {"__builtins__": safe_builtins, **preloaded_modules}
    exec_locals: dict = {}

    # Define a timeout via signal.alarm (Unix-only, main thread requirement)
    def _timeout_handler(signum, frame):
        raise TimeoutError("Execution timed out")

    previous_handler = signal.getsignal(signal.SIGALRM)
    try:
        if timeout_seconds and timeout_seconds > 0:
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout_seconds)

        # Determine if code is a single expression
        is_expr = False
        try:
            compiled_expr = compile(code, "<user_code>", mode="eval")
            is_expr = True
        except SyntaxError:
            compiled_expr = compile(code, "<user_code>", mode="exec")

        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            if is_expr:
                try:
                    value = eval(compiled_expr, exec_globals, exec_locals)
                except Exception as e:
                    return f"Error: {e}"
                finally:
                    signal.alarm(0)
                # Prefer stringified value; if empty, fall back to captured output
                value_str = repr(value)
                out = stdout_buffer.getvalue()
                err = stderr_buffer.getvalue()
                if err:
                    return f"Error: {err.strip()}"
                return value_str if value_str is not None else out
            else:
                try:
                    exec(compiled_expr, exec_globals, exec_locals)
                except Exception as e:
                    return f"Error: {e}"
                finally:
                    signal.alarm(0)
                out = stdout_buffer.getvalue()
                err = stderr_buffer.getvalue()
                if err:
                    return f"Error: {err.strip()}"
                # If the user set a variable named 'result', return it; else return stdout
                if "result" in exec_locals:
                    try:
                        return repr(exec_locals["result"])  # represent safely
                    except Exception:
                        return str(exec_locals["result"])  # fallback
                return out if out else ""
    finally:
        # Restore previous alarm handler
        try:
            signal.alarm(0)
        except Exception:
            pass
        try:
            if previous_handler is not None:
                signal.signal(signal.SIGALRM, previous_handler)
        except Exception:
            pass


if __name__ == "__main__":
    pass
