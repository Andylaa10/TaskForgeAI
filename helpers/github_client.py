# Load environment variables from .env file
import os

from dotenv import load_dotenv

load_dotenv()
class GithubClient:
    github_api_key = os.getenv("GITHUB_API_KEY")
    github_graphql_api_url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {github_api_key}",
        "Content-Type": "application/json"
    }

