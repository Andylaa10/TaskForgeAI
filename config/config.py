﻿import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# mistral_api_key = os.getenv("OPENAI_API_KEY")
azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_openai_api_endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")

LLM_CONFIG = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": azure_openai_api_key,
            "api_type": "azure",
            "base_url": azure_openai_api_endpoint,
            "api_version": "2024-02-01",
            "stream": False,
            "cache_seed": None,
        }
    ],
}

# LLM_CONFIG = {
#     "config_list": [
#         {
#             "model": "open-mistral-nemo", # model name from the Mistral AI API docs
#             "api_key": mistral_api_key,
#             "api_type": "mistral", # the API type is always mistral
#             "api_rate_limit": 0.25, # the rate limit is 0.25 api requests per second
#             "num_predict": -1, # no limit on the number of tokens to predict
#             "repeat_penalty": 1.1, # no penalty for repeating tokens
#             "seed": 42, # the seed is 42
#             "stream": False,
#             "temperature": 0.5, # no temperature
#             "top_k": 50, # top k is 50
#             "top_p": 0.8, # top p is 0.8
#             "native_tool_calls": False, # no native tool calls
#             "cache_seed": None, # no cache seed
#         }
#     ]
# }
