# Utility function to read a high-level task from a file
import json
from typing import List, Annotated

from models.task import Task


def read_task_from_file(file_path: str) -> str:
    """
    Read the high-level task from a file.

    Args:
        file_path (str): Path to the file containing the high-level task.

    Returns:
        str: The high-level task content.
    """
    with open(file_path, 'r') as file:
        data = file.read()
        print(f"File Content: {data}")  # Debug output
        return data

