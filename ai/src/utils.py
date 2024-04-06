import json

# Config filepath
CONFIG_FILE = "config.json"


def load_config(config_file_path=CONFIG_FILE):
    """
    Load the configuration file
    :param config_file_path: Path to the configuration file
    :return: Configuration as a dictionary
    """
    try:
        with open(config_file_path, "r", encoding="utf-8") as fp:
            config = json.load(fp)
    except FileNotFoundError:
        print("ERROR: Config file not found! Please create a config file.")
        exit(1)
    except json.JSONDecodeError:
        print("ERROR: Config file is not a valid JSON file!")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        exit(1)

    return config
