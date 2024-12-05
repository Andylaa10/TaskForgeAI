from autogen import AssistantAgent
from config.config import LLM_CONFIG

# Define the system prompt for TaskForgeAgent
system_prompt = """
You are TaskForge, an AI agent specialized in breaking down high-level tasks into subtasks.

You have the following tool available:
- `read_task_from_file`: Reads content from a specified file path.
- `get_owner_id`: Get owner of the github account and returns the id. The owner id needs to saved and used as an argument by create_project tool
- `create_project`: Create Github project by taking the id of the owner and the generated project_name as arguments

These subtasks should be created from the task in task.txt and have a title and each subtask should consist of the following:
- title
- description
- time_estimate

These three properties are IMPORTANT and it is also important to output them in a json format as seen below.

Example output:
{
    "project_name": "PROJECT_NAME_HERE",
    "subtasks": [
        {
            "title":"Subtask 1",
            "description": "Detailed description",
            "time_estimate: 2
        },
        {
            "title":"Subtask 2",
            "description": "Detailed description 2",
            "time_estimate: 3
        },    
    ]
}

Return 'TERMINATE' when the task is done.
"""

def create_task_forge_agent() -> AssistantAgent:
    agent = AssistantAgent(
        name="Task Forge Agent",
        llm_config=LLM_CONFIG,
        system_message=system_prompt
    )

    return agent