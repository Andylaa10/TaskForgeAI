from typing import Annotated

import requests

from helpers.github_client import GithubClient

def create_project(owner_id: Annotated[str, "Id of the GitHub project owner"], github_client: GithubClient):
    """
    Creates GitHub project
    :param owner_id:
    :param github_client:
    :return:
    """

    query_create_project = """    
    mutation($name: String!, $ownerId: ID!) {    
        createProjectV2(input: {title: $name, ownerId: $ownerId}) {    
            projectV2 {    
                id    
                title    
            }    
        }    
    }    
    """
    variables = {
        "name": "Test Project nr. 123123",
        "ownerId": owner_id,
    }

    response = requests.post(
        url=github_client.github_graphql_api_url,
        headers=github_client.headers,
        json={"query": query_create_project, "variables": variables}
    )

    if response.status_code == 200:
        project_data = response.json()
        project_id = project_data["data"]["createProjectV2"]["projectV2"]["id"]
        return project_id
    else:
        print("Failed to create project. Response:", response.json())
        exit()
