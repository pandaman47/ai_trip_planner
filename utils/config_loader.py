import yaml
import os
from dotenv import load_dotenv
load_dotenv()

def load_config(config_filepath: str = "config/config.yaml") -> dict:
    with open(config_filepath, 'r') as file:
        config = yaml.safe_load(file)
        print(config)

    return config