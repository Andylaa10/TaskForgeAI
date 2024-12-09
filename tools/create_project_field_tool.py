from typing import Annotated
import requests

from helpers.github_client import GithubClient

def create_project_field(projectId: Annotated[str, "ID of the GitHub Project"]) -> Annotated[str, "Id of the newly created Github Prject Field"]:
    github_client = GithubClient()

    query_create_project_field = """
    mutation($dataType: ProjectV2CustomFieldType!, $name: String!, $projectId: ID!, $singleSelectOptions: [ProjectV2SingleSelectFieldOptionInput!]) {
        createProjectV2Field(input: {dataType: $dataType, name: $name, projectId: $projectId, singleSelectOptions: $singleSelectOptions}) {
            projectV2Field {
                ... on ProjectV2Field {
                    id
                    name
                }
            }
        }
    }
    """
    variables = {
        'dataType': 'NUMBER',
        'name': 'Time Estimate',
        'projectId': projectId,
    }

    payload = {
        'query': query_create_project_field,
        'variables': variables
    }

    try:
        response = requests.post(github_client.github_graphql_api_url, headers=github_client.headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            print("Errors:", data["errors"])
            return None

        project_field = data["data"]["createProjectV2Field"]["projectV2Field"]
        return project_field

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None