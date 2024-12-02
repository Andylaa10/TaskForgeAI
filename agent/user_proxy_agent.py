from autogen import ConversableAgent


def create_user_proxy():
    user_proxy = ConversableAgent(
        name="User Proxy",
        llm_config=False,
        is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
        human_input_mode="NEVER",
    )

    return user_proxy