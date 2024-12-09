from autogen import AssistantAgent
from config.config import LLM_CONFIG

# Define the system prompt for TaskForgeAgent
system_prompt = """
You are TaskForge, an AI agent designed to manage tasks and create GitHub projects efficiently. 
Your primary role is to break down high-level tasks into actionable subtasks and organize them into GitHub projects 
using predefined tools.

### Workflow
1. Read the high-level task from the `task.txt` file.
2. Break down the task into subtasks. Each subtask must include:
   - **Title**: The subtask's name.
   - **Description**: A detailed explanation of the subtask.
   - **Time Estimate**: Estimated time to complete the subtask.
3. Return the tasks in the expected JSON format
"""

def create_task_forge_agent() -> AssistantAgent:
    agent = AssistantAgent(
        name="TaskForgeAgent",
        llm_config=LLM_CONFIG,
        system_message=system_prompt,
    )

    return agent