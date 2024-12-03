from autogen import register_function

from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from helpers.file_reader import read_task_from_file, retrieve_task


def setup_agents():
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
    task_forge_agent, user_proxy = setup_agents()

    chat_res = user_proxy.initiate_chat(
        task_forge_agent,
        message = "Read the content of the file at task.txt using the available tool."
    )

    content = chat_res.chat_history[1]["content"]

    for task in retrieve_task(content):
        print(task.title)
        print(task.description)
        print(task.time_estimate)

if __name__ == '__main__':
    main()