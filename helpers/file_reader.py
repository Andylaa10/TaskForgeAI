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

def retrieve_task(content) -> Annotated[List[Task], "Returns a list of the generate tasks with title, description and time_estimates"]:
    """
    Iterates through the string to get the title, description and time_estimate
    :param content:
    :return:
    """
    tasks: List[Task] = []
    # Remove terminate from our json object
    if "TERMINATE" in content:
        content = content.split("TERMINATE")[0].strip()
    data = json.loads(content)
    subtasks = data["subtasks"]
    time_estimates = data["time_estimates"]
    for task in subtasks:
        title = task['title']
        description = task['description']
        time = None
        for estimate in time_estimates:
            if title in estimate:
                time = estimate[title]
                break
        if time is not None:
            tasks.append(Task(title, description, time))
        else:
            print(f"No time estimate found for task: {title}")
    return tasks