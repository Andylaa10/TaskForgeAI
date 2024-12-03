from autogen import register_function

from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from helpers.file_reader import read_task_from_file, retrieve_task


def setup_agents():
    """
    Initialize and set up TaskForgeAgent and UserProxy with the registered file-reading tool.
    """
    task_forge_agent = create_task_forge_agent()
    user_proxy = create_user_proxy()

    register_function(
        read_task_from_file,
        caller=task_forge_agent,
        executor=user_proxy,
        name="read_content_of_file",  # Match this name to the system prompt
        description="Read content from a file",
    )

    return task_forge_agent, user_proxy


def main():
    # Set up agents
    task_forge_agent, user_proxy = setup_agents()

    # Start the conversation with the TaskForge agent
    try:
        print("[DEBUG] Initiating chat with TaskForge agent...")
        chat_res = user_proxy.initiate_chat(
            task_forge_agent,
            message="Read the content of the file at task.txt using the available tool (read_content_of_file)."
        )

        # Extract and process the content
        content = chat_res.chat_history[1]["content"]
        print("[DEBUG] Retrieved Content from Agent:", content)

        # Process tasks
        tasks = retrieve_task(content)
        if not tasks:
            print("[ERROR] No tasks retrieved from agent's response.")
            return

        for task in tasks:
            print(f"Task Title: {task.title}")
            print(f"Task Description: {task.description}")
            print(f"Task Time Estimate: {task.time_estimate} hours")

    except Exception as e:
        print(f"[ERROR] An exception occurred: {e}")


if __name__ == '__main__':
    main()
