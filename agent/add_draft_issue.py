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
        return draft_issue_data
    else:
        print("Failed to add draft issue. Response:", response.json())
        exit()


def main():
    # Replace with the actual project ID retrieved from the first script.
    project_id = "PVT_kwHOBXSci84AthMs"

    # Example draft issues
    issues = [
        {"title": "Draft Issue 1", "body": "This is the body of draft issue 1."},
        {"title": "Draft Issue 2", "body": "This is the body of draft issue 2."},
        {"title": "Draft Issue 3", "body": "This is the body of draft issue 3."}
    ]

    for issue in issues:
        add_project_v2_draft_issue(project_id, issue["title"], issue["body"])


if __name__ == "__main__":
    main()
