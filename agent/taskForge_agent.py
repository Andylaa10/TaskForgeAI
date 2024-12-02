from autogen import ConversableAgent
# from config import LLM_CONFIG

LLM_CONFIG = {
    "model": "mistral:latest",
    "client_host": "http://localhost:11434/",
    "api_type": "ollama",
    "seed": 42,
    "cache_seed": None,
    "repeat_penalty": 1.1,
    "stream": False,
    "native_tool_calls": False,
    "temp": 0.0,
    "use_docker": False,
}

# Define the system prompt for TaskForgeAgent
system_prompt = """
You are TaskForge, an AI agent specialized in breaking down high-level tasks into actionable subtasks. 
You will estimate the time and cost required for each subtask. Use any available tools to gather necessary 
information for accurate estimations. Return your response in JSON format containing `subtasks`, `time_estimates`, 
and `cost_estimates`.

Example output:
{
    "subtasks": [
        {"name": "Subtask 1", "description": "Detailed description"},
        {"name": "Subtask 2", "description": "Detailed description"}
    ],
    "time_estimates": {"Subtask 1": "2 hours", "Subtask 2": "3 hours"},
    "cost_estimates": {"Subtask 1": "$50", "Subtask 2": "$75"}
}

Only return the JSON response.
"""

class TaskForgeAgent:
    def __init__(self):
        self.agent = self.create_agent()

    def create_agent(self) -> ConversableAgent:
        return ConversableAgent(
            name="taskForge_agent",
            llm_config=LLM_CONFIG,
            system_message=system_prompt
        )

    def process_task(self, high_level_task: str) -> dict:  # Indented correctly now
        """
        Process a high-level task and return subtasks, time estimates, and cost estimates.

        Args:
            high_level_task (str): The high-level task to process.

        Returns:
            dict: JSON object containing subtasks, time, and cost estimates.
        """
        messages = [{"role": "user", "content": high_level_task}]  # Structured message
        response = self.agent.generate_reply(messages=messages, sender="user")
        return response

# Utility function to read a high-level task from a file
def read_task_from_file(file_path: str) -> str:
    """
    Read the high-level task from a file.

    Args:
        file_path (str): Path to the file containing the high-level task.

    Returns:
        str: The high-level task content.
    """
    with open(file_path, "r") as file:
        return file.read().strip()

# Example usage
if __name__ == "__main__":
    # Instantiate TaskForgeAgent
    task_forge = TaskForgeAgent()

    # Read task from a file
    task_file = r"C:\Users\Kristian\Documents\GitHub\TaskForgeAI\agent\task.txt"
    high_level_task = read_task_from_file(task_file)

    # Process the task
    breakdown = task_forge.process_task(high_level_task)

    # Print the result
    print(breakdown)