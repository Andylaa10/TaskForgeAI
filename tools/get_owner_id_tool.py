from typing import Annotated
import requests

from helpers.github_client import GithubClient

def get_owner_id() -> Annotated[str, "Id of the owner"]:
    """
    Get the owner of the GitHub project
    :param github_client:
    :return:
    """
    
    github_client = GithubClient()
    query_get_id = """    
    query {    
        viewer {    
            id    
            login    
        }    
    }    
    """
    response = requests.post(
        url=github_client.github_graphql_api_url,
        headers=github_client.headers,
        json={"query": query_get_id}
    )

    if response.status_code == 200:
        viewer_data = response.json()
        return str(viewer_data["data"]["viewer"]["id"])