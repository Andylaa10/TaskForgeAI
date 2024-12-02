import requests

GITHUB_API_KEY = ""
GITHUB_GRAPHQL_API = "https://api.github.com/graphql"

query_get_id = """
query {
    viewer {
        id
        login
    }
}
"""

headers = {
    "Authorization": f"Bearer {GITHUB_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(
    url=GITHUB_GRAPHQL_API,
    headers=headers,
    json={"query": query_get_id}
)

if response.status_code == 200:
    viewer_data = response.json()
    owner_id = viewer_data["data"]["viewer"]["id"]
    print("Fetched owner ID:", owner_id)
else:
    print("Failed to fetch owner ID. Response:", response.json())
    exit()

query_create_project = """
mutation($name: String!) {
    createProjectV2(input: {title: $name, ownerId: ""}) {
        projectV2 {
            id
            title
        }
    }
}
"""
variables = {
    "name": "Test Project",
    "ownerId": ""
}

response = requests.post(
    url=GITHUB_GRAPHQL_API,
    headers=headers,
    json={"query": query_create_project, "variables": variables}
)

if response.status_code == 200:
    print("Project created successfully:", response.json())
else:
    print("Failed to create project. Response:", response.json())