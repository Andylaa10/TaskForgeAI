import requests
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key
GITHUB_API_KEY = os.getenv("GITHUB_API_KEY")
GITHUB_GRAPHQL_API = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {GITHUB_API_KEY}",
    "Content-Type": "application/json"
}


def get_owner_id():
    query_get_id = """    
    query {    
        viewer {    
            id    
            login    
        }    
    }    
    """
    response = requests.post(
        url=GITHUB_GRAPHQL_API,
        headers=headers,
        json={"query": query_get_id}
    )

    if response.status_code == 200:
        viewer_data = response.json()
        return viewer_data["data"]["viewer"]["id"]
    else:
        print("Failed to fetch owner ID. Response:", response.json())
        exit()


def create_project(owner_id):
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
        url=GITHUB_GRAPHQL_API,
        headers=headers,
        json={"query": query_create_project, "variables": variables}
    )

    if response.status_code == 200:
        project_data = response.json()
        project_id = project_data["data"]["createProjectV2"]["projectV2"]["id"]
        return project_id
    else:
        print("Failed to create project. Response:", response.json())
        exit()


def main():
    owner_id = get_owner_id()
    print("Owner_ID:", owner_id)

    project_id = create_project(owner_id)
    print("Project_ID:", project_id)

    print("GREAT SUCCESS")


if __name__ == "__main__":
    main()