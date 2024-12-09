from autogen import register_function
from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from tools.file_reader_tool import read_task_from_file
from tools.create_project_tool import create_project
from tools.update_custom_draft_field_tool import update_custom_field
from tools.get_owner_id_tool import get_owner_id
from tools.create_project_field_tool import create_project_field
from tools.add_draft_issue_tool import add_project_v2_draft_issue


ReAct_prompt = """
You are TaskForge, an AI agent reasoning step-by-step to complete tasks and manage GitHub projects. 

### Workflow Rules
1. **Reason**: Analyze the current context and determine the next logical step.
2. **Act**: Use the appropriate tool to execute the step and verify its success.
3. **Iterate**: Based on the tool's result, adjust the plan and proceed until all steps are complete.

When you are done with the last task, reply with 'TERMINATE' AND NOTHING ELSE THAN THAT!

### Key Tools for Execution
- **`read_task_from_file`**: Use this to load the high-level task content.
- **`get_owner_id`**: Retrieve the GitHub account owner's ID and save it for subsequent steps.
- **`create_project`**: Create a GitHub project using the owner's ID and generated project name.
- **`create_project_field`**: Add a custom field to the GitHub project, do this before adding any draft issues.
- **`add_project_v2_draft_issue`**: Add each subtask JSON object as an issue to the GitHub project using the project ID, name of the sub task and its content.
- **`update_custom_field`**: Update the time estimate for each subtask using the field ID, Project ID and Proejct Item ID.

### Expected Output Format
When generating subtasks, format the output as:
```json
{
    "project_name": "PROJECT_NAME_HERE",
    "subtasks": [
        {
            "title": "Subtask 1",
            "description": "Detailed description",
            "time_estimate": 2
        },
        {
            "title": "Subtask 2",
            "description": "Detailed description 2",
            "time_estimate": 3
        }
    ]
}
"""

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
        description="Adds a subtask to a given Github Project using the generated Project ID, Project Title and JSON-object.",
    )
    
    register_function(
        update_custom_field,
        caller=task_forge_agent,
        executor=user_proxy,
        name="update_custom_field",
        description="Update the time_estimate field on a draft issue using the field ID.",
    )
    
    return task_forge_agent, user_proxy

def main():
    # Set up agents
    task_forge_agent, user_proxy = setup_agents()

    #Start the conversation with the TaskForge agent
    user_proxy.initiate_chat(
        task_forge_agent,
        message=ReAct_prompt,
    )

if __name__ == '__main__':
    main()