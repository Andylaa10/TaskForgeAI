import requests

from helpers.github_client import GithubClient

def get_owner_id(github_client: GithubClient):
    """
    Get the owner of the GitHub project
    :param github_client:
    :return:
    """
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
        return viewer_data["data"]["viewer"]["id"]
    else:
        print("Failed to fetch owner ID. Response:", response.json())
        exit()