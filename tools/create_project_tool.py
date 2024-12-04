from typing import Annotated
import requests

class CreateProjectTool:
    def __init__(self, github_client):
        """
        Initialize the Create Project Tool with a GitHub client.
        :param github_client: Instance of GithubClient
        """
        self.github_client = github_client

    def create_project(self, owner_id: Annotated[str, "ID of the GitHub project owner"], project_name: str):
        """
        Create a GitHub project.
        :param owner_id: The ID of the GitHub project owner.
        :param project_name: The name of the project to create.
        :return: The ID of the created project.
        """
        query = """    
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
            "name": project_name,
            "ownerId": owner_id,
        }

        response = requests.post(
            url=self.github_client.github_graphql_api_url,
            headers=self.github_client.headers,
            json={"query": query, "variables": variables}
        )

        if response.status_code == 200:
            project_data = response.json()
            return project_data["data"]["createProjectV2"]["projectV2"]["id"]
        else:
            raise Exception(f"Failed to create project: {response.json()}")