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