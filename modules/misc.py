import logging
import os
import json


def save_results(results, save_dir, filename):
    os.makedirs(save_dir, exist_ok=True)

    type = filename.split(".")[-1]

    path = os.path.join(save_dir, filename)

    if type == "json":
        with open(path, "w") as file:
            try:
                json.dump(results, file, indent=3)
                logging.info(f"Saving successfully to {path}")
            except Exception as e:
                logging.error(f"Failed saving {filename}: {e}")

    elif type == "txt":
        with open(path, "w") as file:
            try:
                for result in results:
                    file.write(f"{result}")
                    logging.info(f"Saving successfully to {path}")
            except Exception as e:
                    logging.error(f"Failed saving {result}: {e}")

def logger_config(tool):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S", # Punt milliseconds
        handlers=[
            logging.FileHandler(os.path.join(tool, "log.txt"))
        ]
)

def load_usernames(name=None, names=None):
    result = []
    
    if name:
        result = [name]
    elif names:
        try:
            with open(names, "r") as file:
                for line in file:
                    result.append(line.strip())
                logging.info(f"Wordlist {names} successfully loaded")
        except FileNotFoundError as e:
            logging.error(f"Username wordlist {names} not found: {e}")
    return result

def load_passwords(password=None, passwords=None):
    result = []
    
    if password:
        result = [password]
    elif passwords:
        try:
            with open(passwords, "r") as file:
                for line in file:
                    result.append(line.strip())
                logging.info(f"Wordlist {passwords} successfully loaded")
        except FileNotFoundError as e:
            logging.error(f"Password wordlist {passwords} not found: {e}")
    return result

class Colors:
    RESET = "\033[0m"  # Default color
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"

