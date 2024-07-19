import logging
import logging.config
from typing import Dict
import os
from pyarrow import compute as pc
import pyarrow as pa
import yaml

def create_logging_config(app_name: str) -> Dict:
    """
    Create a logging configuration dictionary with dynamic log filenames.

    Args:
        app_name (str): The name of the application.

    Returns:
        Dict: The logging configuration dictionary.
    """
    date_str = pc.strftime(pa.scalar(pa.now()), format='%d%m').as_py()
    prefix = app_name[:2].lower()

    log_filename_1 = f"filebeat-{prefix}_{date_str}.log"
    log_filename_2 = f"filebeat-{prefix}_{date_str}.log"

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file1': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'filename': log_filename_1
            },
            'file2': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'filename': log_filename_2
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'file1', 'file2']
        }
    }

    return logging_config

def setup_logging(app_name: str) -> None:
    """
    Set up logging configuration for the application.

    Args:
        app_name (str): The name of the application.
    """
    logging_config = create_logging_config(app_name)

    # Write the logging configuration to a YAML file for reference
    with open('logging_config.yaml', 'w') as file:
        yaml.dump(logging_config, file)

    # Apply the logging configuration
    logging.config.dictConfig(logging_config)

# Example usage
app_name = __name__
print(app_name)
setup_logging(app_name)

logger = logging.getLogger(app_name)
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.error("This is an error message")