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
You will estimate the title and time required for each subtask (in hours). Use any available tools to gather necessary 
information for accurate estimations. Return your response in JSON format containing `subtasks` & `time_estimates`.
Example output:
{
    "subtasks": [
        {"name": "Subtask 1", "description": "Detailed description"},
        {"name": "Subtask 2", "description": "Detailed description"}
    ],
    "time_estimates": {"Subtask 1": "2 hours", "Subtask 2": "3 hours"},
}

Only return the JSON response.

When all steps above are done:
 - Write TERMINATE (it should always be UPPERCASE and the last word in the response at all time)
 
"""


def create_task_forge_agent() -> ConversableAgent:
    # Define the agent
    agent = ConversableAgent(
        name="Task Forge Agent",
        llm_config=LLM_CONFIG,
        system_message=system_prompt
    )

    return agent


def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User Proxy",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    return user_proxy


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
    with open(file_path, 'r') as file:
        data = file.read()
        return data


def main():
    file = read_task_from_file("task.txt")
    task_forge_agent = create_task_forge_agent()
    user_proxy = create_user_proxy()
    user_proxy.initiate_chat(
        task_forge_agent,
        message=file
    )


# Example usage
if __name__ == "__main__":
    main()
