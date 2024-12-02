from agent.taskForge_agent import create_task_forge_agent
from agent.user_proxy_agent import create_user_proxy
from helpers.file_reader import read_task_from_file, retrieve_task


def main():
    file = read_task_from_file("task.txt")
    task_forge_agent = create_task_forge_agent()
    user_proxy = create_user_proxy()

    chat_res = user_proxy.initiate_chat(
        task_forge_agent,
        message=file,
        summary_method="reflection_with_llm",
    )

    content = chat_res.chat_history[1]["content"]

    for task in retrieve_task(content):
        print(task.title)
        print(task.description)
        print(task.time_estimate)
    

if __name__ == '__main__':
    main()