from autogen import register_function
from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from helpers.file_reader import read_task_from_file
from helpers.github_client import GithubClient
from tools.create_project_tool import create_project
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
        name="read_task_from_file",  # Match this name to the system prompt
        description="Reads the content of the selected file.",
    )
    
    register_function(
        get_owner_id,
        caller=task_forge_agent,
        executor=user_proxy,
        name="get_owner_id",
        description="Get owner of the github account and returns the id. The owner id needs to saved and used as an argument by create_project tool.",
    )
    
    register_function(
        create_project,
        caller=task_forge_agent,
        executor=user_proxy,
        name="create_project",
        description="Create Github project by taking the id of the owner and the generated project_name as arguments.",
    )

    register_function(
        create_project_field,
        caller=task_forge_agent,
        executor=user_proxy,
        name="create_project_field",
        description="Create a custom field inside the Github Project by using the generated Project ID.",
    )

    register_function(
        add_project_v2_draft_issue,
        caller=task_forge_agent,
        executor=user_proxy,
        name="add_project_v2_draft_issue",
        description="Add the subtasks to the Github Project using the generated Project ID, Project Title and JSON-object.",
    )
    
    return task_forge_agent, user_proxy

def create_project_and_subtasks(github_client, task_forge_agent, user_proxy):
    """
    Logic to create a project, fields, and subtasks based on content from task file.
    """
    try:
        #Start the conversation with the TaskForge agent
        user_proxy.initiate_chat(
            task_forge_agent,
            message="Read the content of the file at task.txt using the available tool (read_task_from_file, get_owner_id, create_project, create_project_field, add_project_v2_draft_issue).",
        )

        # owner_id = get_owner_id(github_client)

        # # Retrieve the last message from task_forge_agent
        # response_content = task_forge_agent.last_message(user_proxy)

        # if 'content' in response_content:
        #     content_data = json.loads(response_content["content"])
        
        # if 'project_name' in content_data:
        #     # Get the project name from the agent response
        #     project_name = content_data["project_name"]
            
        #     # Create the project and get the project ID
        #     project_id = create_project(owner_id, project_name)
            
        #     # Create the project field and get the project field ID
        #     project_field_data = create_project_field(project_id, github_client)
        #     project_field_id = project_field_data['id']
        
        # if "subtasks" in content_data:
        #     subtasks_data = content_data["subtasks"]
        
        # for subtask in subtasks_data:
        #     title = subtask["title"]
        #     body = subtask['description']
        #     time_estimate = subtask['time_estimate']
            
        #     draft_issue_id = add_project_v2_draft_issue(project_id, title, body, github_client)
            
        #     update_custom_field(project_id, draft_issue_id, project_field_id, time_estimate, github_client)

    except Exception as e:
        print(f"[ERROR] An exception occurred: {e}")

def main():
    # Set up agents
    task_forge_agent, user_proxy = setup_agents()

    # Initialize GitHub client
    github_client = GithubClient()

    # Create project and subtasks
    create_project_and_subtasks(github_client, task_forge_agent, user_proxy)

if __name__ == '__main__':
    main()