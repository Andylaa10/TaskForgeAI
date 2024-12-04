from autogen import register_function

from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from helpers.file_reader import read_task_from_file
from helpers.github_client import GithubClient
from tools.create_project_tool import CreateProjectTool
from tools.update_custom_draft_field_tool import update_custom_field
from tools.get_owner_id_tool import get_owner_id
from tools.create_project_field import create_project_field
from tools.add_draft_issue_tool import add_project_v2_draft_issue

import json



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
    global subtasks_data, content_data
    task_forge_agent, user_proxy = setup_agents()

    # Initialize GitHub client and CreateProjectTool
    github_client = GithubClient()
    create_project_tool = CreateProjectTool(github_client)

    try:
        # Start the conversation with the TaskForge agent
        user_proxy.initiate_chat(
            task_forge_agent,
            message="Read the content of the file at task.txt using the available tool (read_content_of_file)."
        )

        owner_id = get_owner_id(github_client)

        # Create a GitHub project for the subtasks
        project_name = "Test Project nr. 123123"

        # Create the project and get the project ID
        project_id = create_project_tool.create_project(owner_id, project_name)
        print(f"Project created successfully with ID: {project_id}")

        # Create the project field and get the project field ID
        project_field_data = create_project_field(project_id, github_client)
        project_field_id = project_field_data['id']
        print(f"Project Field created successfully with ID: {project_field_id}")

        # Retrieve the last message from task_forge_agent
        response_content = task_forge_agent.last_message(user_proxy)

        print("Response Content:", response_content)

        if 'content' in response_content:
            content_data = json.loads(response_content["content"])
        if "subtasks" in content_data:
            subtasks_data = content_data["subtasks"]
        for subtask in subtasks_data:
            title = subtask["title"]
            body = subtask['description']
            time_estimate = subtask['time_estimate']
            print("title: ", title, "description: ", body, "time_estimate: ", time_estimate)
            draft_issue_id = add_project_v2_draft_issue(project_id, title, body, github_client)
            print('draft issue:',draft_issue_id)
            updated_field_id = update_custom_field(project_id, draft_issue_id, project_field_id, time_estimate, github_client)
            print('updated field ID:', updated_field_id)
            

    except Exception as e:
        print(f"[ERROR] An exception occurred: {e}")


if __name__ == '__main__':
    main()
