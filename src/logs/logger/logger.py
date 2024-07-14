# Logger class
import os
import logging
import logging.config
from dotenv import load_dotenv

class LoggerConfig:
    def __init__(self, config_path):
        load_dotenv()
        self.config_path = config_path
        self.load_configuration()

    def load_configuration(self):
        """Load logging configuration from a YAML file."""
        import yaml
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file.read())
            logging.config.dictConfig(config)

class AppLogger:
    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Example of initializing the LoggerConfig and AppLogger
if __name__ == "__main__":
    # Initialize logging
    config = LoggerConfig('path_to_logging_config.yaml')
    app_logger = AppLogger(__name__)