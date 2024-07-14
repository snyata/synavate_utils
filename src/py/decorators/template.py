from functools import wraps
from time import time
from typing import Any, Callable, Type
from pydantic import BaseModel, ValidationError

def timer(func: Callable) -> Callable:
    """
    Decorator to measure the execution time of a function.
    
    Args:
        func (Callable): The function to measure.

    Returns:
        Callable: The wrapped function with timing.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

def validate_with_schema(schema_model: Type[BaseModel]) -> Callable:
    """
    Decorator to validate function arguments with a Pydantic schema.

    Args:
        schema_model (Type[BaseModel]): The Pydantic model to validate against.

    Returns:
        Callable: The wrapped function with validation.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                schema_model(**kwargs)
            except ValidationError as e:
                print(f"Validation error: {e}")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

def retry_on_exception(max_retries: int = 3) -> Callable:
    """
    Decorator to retry a function if an exception occurs.

    Args:
        max_retries (int): The maximum number of retries. Default is 3.

    Returns:
        Callable: The wrapped function with retry logic.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == max_retries:
                        raise
        return wrapper
    return decorator

def log_function_call(func: Callable) -> Callable:
    """
    Decorator to log function calls with arguments and return values.

    Args:
        func (Callable): The function to log.

    Returns:
        Callable: The wrapped function with logging.
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Calling '{func.__name__}' with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"'{func.__name__}' returned: {result}")
        return result
    return wrapper

def singleton(cls: Type) -> Type:
    """
    Decorator to make a class a singleton.

    Args:
        cls (Type): The class to make singleton.

    Returns:
        Type: The singleton class.
    """
    instances = {}

    @wraps(cls)
    def get_instance(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

# Example Pydantic model for validation
class LogSchema(BaseModel):
    timestamp: str
    event_type: str
    entities: list[str]

# Example usage of the decorators
@timer
@validate_with_schema(LogSchema)
@retry_on_exception(max_retries=5)
@log_function_call
def process_log_data(timestamp: str, event_type: str, entities: list[str]) -> None:
    if event_type not in {"INFO", "ERROR", "WARN", "DEBUG"}:
        raise ValueError("Invalid event_type")
    print(f"Processing log data: {timestamp}, {event_type}, {entities}")

# Using the singleton decorator
@singleton
class Config:
    def __init__(self, name: str) -> None:
        self.name = name

# Example invocation
if __name__ == "__main__":
    process_log_data(
        timestamp="2023-07-10 10:00:00",
        event_type="INFO",
        entities=["Device_A"]
    )

    # Singleton usage
    config1 = Config(name="config1")
    config2 = Config(name="config2")
    print(config1 is config2)  # Should print True
