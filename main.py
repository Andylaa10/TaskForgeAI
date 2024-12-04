from autogen import register_function

from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from helpers.file_reader import read_task_from_file, retrieve_task
from helpers.github_client import GithubClient
from tools.create_project_tool import CreateProjectTool
import os


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

    # Initialize GitHub client and CreateProjectTool
    github_client = GithubClient()
    create_project_tool = CreateProjectTool(github_client)

    try:
        # Start the conversation with the TaskForge agent
        chat_res = user_proxy.initiate_chat(
            task_forge_agent,
            message="Read the content of the file at task.txt using the available tool (read_content_of_file)."
        )

        # Create a GitHub project for the subtasks
        project_name = "Test Project nr. 123123"
        project_id = create_project_tool.create_project(github_client.owner_id, project_name)
        print(f"Project created successfully with ID: {project_id}")


        # Extract and process the content
       # content = chat_res.chat_history[1]["content"]

        # Process tasks
       # tasks = retrieve_task(content)
        #if not tasks:
        #    return

      #  for task in tasks:
      #      print(f"Task Title: {task.title}")
      #      print(f"Task Description: {task.description}")
      #      print(f"Task Time Estimate: {task.time_estimate} hours")

    except Exception as e:
        print(f"[ERROR] An exception occurred: {e}")


if __name__ == '__main__':
    main()
