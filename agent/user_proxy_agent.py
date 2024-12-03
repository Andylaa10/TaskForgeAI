from autogen import UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor
import tempfile




def create_user_proxy():
    temp_dir = tempfile.TemporaryDirectory()

    code_executor_config = LocalCommandLineCodeExecutor(
        timeout=30,
        work_dir=temp_dir.name,
    )
    
    user_proxy = UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        code_execution_config={"executor": code_executor_config},
    )


    return user_proxy