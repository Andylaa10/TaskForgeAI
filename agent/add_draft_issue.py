import requests

GITHUB_API_KEY = ""
GITHUB_GRAPHQL_API = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {GITHUB_API_KEY}",
    "Content-Type": "application/json"
}


def add_project_v2_draft_issue(project_id, title, body):
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
        url=GITHUB_GRAPHQL_API,
        headers=headers,
        json={"query": query_add_draft_issue, "variables": variables}
    )

    if response.status_code == 200:
        draft_issue_data = response.json()
        print("Draft issue added:", draft_issue_data)
        return draft_issue_data["data"]["addProjectV2DraftIssue"]["projectItem"]["id"]
    else:
        print("Failed to add draft issue. Response:", response.json())
        exit()


def update_custom_field(project_id, project_item_id, field_id, value):
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
    # Format the value object for the field (adjust based on your field type)
    formatted_value = {"number": value}

    variables = {
        "projectId": project_id,
        "projectItemId": project_item_id,
        "fieldId": field_id,
        "value": formatted_value
    }

    response = requests.post(
        url=GITHUB_GRAPHQL_API,
        headers=headers,
        json={"query": query_update_field, "variables": variables}
    )

    if response.status_code == 200:
        print(f"Field {field_id} updated successfully for item {project_item_id}")
        print("Response:", response.json())  # Keep for debugging
    else:
        print("Failed to update custom field. Response:", response.json())


def main():
    # Replace with your actual project and field IDs
    project_id = "PVT_kwHOBWsYlM4Athd3"  # The project ID
    time_estimate_field_id = "PVTF_lAHOBWsYlM4Athd3zgkRNT8"  # The ID of your Time Estimate field

    # Example draft issues
    issues = [
        {"title": "Draft Issue 145", "body": "This is the body of draft issue 1.", "Time Estimate": 1},
        {"title": "Draft Issue 25", "body": "This is the body of draft issue 2.", "Time Estimate": 3},
        {"title": "Draft Issue 37", "body": "This is the body of draft issue 3.", "Time Estimate": 7}
    ]

    for issue in issues:
        # Step 1: Add the draft issue and get its ID
        project_item_id = add_project_v2_draft_issue(project_id, issue["title"], issue["body"])

        # Step 2: Update custom fields for the draft issue
        update_custom_field(project_id, project_item_id, time_estimate_field_id, issue["Time Estimate"])


if __name__ == "__main__":
    main()
