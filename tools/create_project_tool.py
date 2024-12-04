﻿from typing import Annotated
import requests

from helpers.github_client import GithubClient

def create_project(owner_id: Annotated[str, "ID of the GitHub project owner"], project_name: str):
        """
        Create a GitHub project.
        :param owner_id: The ID of the GitHub project owner.
        :param project_name: The name of the project to create.
        :return: The ID of the created project.
        """

        github_client = GithubClient()

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
            url=github_client.github_graphql_api_url,
            headers=github_client.headers,
            json={"query": query, "variables": variables}
        )

        if response.status_code == 200:
            project_data = response.json()
            return project_data["data"]["createProjectV2"]["projectV2"]["id"]
        else:
            raise Exception(f"Failed to create project: {response.json()}")