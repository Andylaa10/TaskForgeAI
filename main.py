from autogen import register_function
from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from helpers.file_reader import read_task_from_file
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
    
    register_function(
        update_custom_field,
        caller=task_forge_agent,
        executor=user_proxy,
        name="update_custom_field",
        description="Update the time_estimate field on a draft issue using the project field ID.",
    )
    
    return task_forge_agent, user_proxy

def main():
    # Set up agents
    task_forge_agent, user_proxy = setup_agents()

    #Start the conversation with the TaskForge agent
    user_proxy.initiate_chat(
        task_forge_agent,
        message="Read the content of the file at task.txt using the available tool (read_task_from_file, get_owner_id, create_project, create_project_field, add_project_v2_draft_issue, update_custom_field).",
    )

if __name__ == '__main__':
    main()