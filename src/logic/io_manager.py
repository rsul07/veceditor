import json
import os

class FileManager:
    """
    Handles low-level file I/O operations.
    Decoupled from Qt logic.
    """

    @staticmethod
    def save_json(filename: str, data: dict):
        """
        Writes a dictionary to a JSON file.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except OSError as e:
            raise IOError(f"Failed to write file: {e}")

    @staticmethod
    def load_json(filename: str) -> dict:
        """
        Reads a JSON file and returns a dictionary.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError("File is corrupted or has invalid format")
        except OSError as e:
            raise IOError(f"Failed to read file: {e}")