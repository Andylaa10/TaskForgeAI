from typing import Annotated
from helpers.github_client import GithubClient

import requests

def update_custom_field(project_id: Annotated[str, "Id of the GitHub project"],
                        project_item_id: Annotated[str, "Id of the draft"],
                        field_id: Annotated[str, "Id of the custom field"],
                        value: Annotated[int, "Numbers only"],
                        github_client: GithubClient):
    """
    Updates a draft with a custom field which in this is time_estimate
    :param project_id:
    :param project_item_id:
    :param field_id:
    :param value:
    :param github_client:
    :return:
    """

    query_update_field = """
    mutation($projectId: ID!, $projectItemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
        updateProjectV2ItemFieldValue(input: {
            projectId: $projectId,
            itemId: $projectItemId,
            fieldId: $fieldId,
            value: $value
        }) {
            clientMutationId  # Optionally, include this for debugging purposes
        }
    }
    """
    formatted_value = {"number": value}

    variables = {
        "projectId": project_id,
        "projectItemId": project_item_id,
        "fieldId": field_id,
        "value": formatted_value
    }

    requests.post(
        url=github_client.github_graphql_api_url,
        headers=github_client.headers,
        json={"query": query_update_field, "variables": variables}
    )