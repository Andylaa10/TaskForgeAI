from typing import Annotated
from helpers.github_client import GithubClient

import requests

def add_project_v2_draft_issue(project_id: Annotated[str, "Id of the GitHub project"],
                               title: Annotated[str, "Name of the new draft"],
                               body: Annotated[str, "Description of the new draft"]) -> Annotated[str, "Id of the newly created draft issue"]:
    
    github_client = GithubClient()

    """
    Adds new draft to GitHub project, it is also a new card in the kanban view
    :param project_id:
    :param title:
    :param body:
    :param github_client:
    :return:
    """

    query_add_draft_issue = """
    mutation($projectId: ID!, $title: String!, $body: String!) {
        addProjectV2DraftIssue(input: {projectId: $projectId, title: $title, body: $body}) {
            projectItem {
                id
            }
        }
    }
    """
    variables = {
        "projectId": project_id,
        "title": title,
        "body": body
    }

    response = requests.post(
        url=github_client.github_graphql_api_url,
        headers=github_client.headers,
        json={"query": query_add_draft_issue, "variables": variables}
    )

    if response.status_code == 200:
        draft_issue_data = response.json()
        return draft_issue_data["data"]["addProjectV2DraftIssue"]["projectItem"]["id"]
    else:
        print("Failed to add draft issue. Response:", response.json())
        exit()