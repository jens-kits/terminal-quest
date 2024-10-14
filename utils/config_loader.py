# TerminalQuest/utils/config_loader.py

import yaml
import os
import logging

logger = logging.getLogger(__name__)

def load_config(file_path):
    """
    Load and parse a YAML configuration file.
    
    Args:
    file_path (str): Path to the YAML configuration file.
    
    Returns:
    dict: Parsed configuration data, or None if there was an error.
    """
    if not os.path.exists(file_path):
        logger.error(f"Configuration file not found: {file_path}")
        return None
    
    try:
        with open(file_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)
        logger.info(f"Successfully loaded configuration from {file_path}")
        logger.debug(f"Configuration contents: {config_data}")
        return config_data
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading configuration: {e}")
        return None

def validate_config(config_data, schema):
    """
    Validate the configuration data against a schema.
    
    Args:
    config_data (dict): Parsed configuration data.
    schema (dict): Schema to validate against.
    
    Returns:
    bool: True if valid, False otherwise.
    
    Note: This is a placeholder function. You might want to use a library like
    'jsonschema' for more robust schema validation.
    """
    # Placeholder implementation
    return True

# Example usage:
# config = load_config('game_config.yaml')
# if validate_config(config, schema):
#     print("Configuration is valid")
# else:
#     print("Configuration is invalid")