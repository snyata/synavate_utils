from pydantic import BaseModel, ValidationError, validator
from typing import Any, Dict, List

class LogSchema(BaseModel):
    timestamp: str
    event_type: str
    entities: List[str]

    @validator('timestamp')
    def timestamp_must_be_valid(cls, v):
        # Add custom validation for timestamp if needed
        return v

    @validator('event_type')
    def event_type_must_be_valid(cls, v):
        # Ensure event_type is one of the expected values
        if v not in {"INFO", "ERROR", "WARN", "DEBUG"}:
            raise ValueError('Invalid event_type')
        return v

def validate_data(data: Dict[str, Any], schema_model: BaseModel) -> bool:
    """
    Validate and enforce a Pydantic schema.

    Args:
        data (Dict[str, Any]): The data to be validated.
        schema_model (BaseModel): The Pydantic model to validate against.

    Returns:
        bool: True if the data is valid according to the schema, False otherwise.
    """
    try:
        schema_model(**data)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False
    return True

# Example usage
data = {
    "timestamp": "2023-07-10 10:00:00",
    "event_type": "INFO",
    "entities": ["Device_A"]
}

is_valid = validate_data(data, LogSchema)
print(f"Is data valid? {is_valid}")