import json
import jsonschema
from jsonschema import validate
from typing import Any, Dict

def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Validate and enforce a JSON schema.

    Args:
        data (Dict[str, Any]): The JSON data to be validated.
        schema (Dict[str, Any]): The JSON schema to validate against.

    Returns:
        bool: True if the data is valid according to the schema, False otherwise.
    """
    try:
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation error: {e.message}")
        return False
    return True

# Example usage
schema = {
    "type": "object",
    "properties": {
        "timestamp": {"type": "string"},
        "event_type": {"type": "string"},
        "entities": {"type": "string"}
    },
    "required": ["timestamp", "event_type", "entities"]
}

data = {
    "timestamp": "2023-07-10 10:00:00",
    "event_type": "INFO",
    "entities": "Device_A"
}

is_valid = validate_json_schema(data, schema)
print(f"Is data valid? {is_valid}")