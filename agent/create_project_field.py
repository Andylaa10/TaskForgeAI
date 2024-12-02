import requests

GITHUB_API_KEY = ""
GITHUB_GRAPHQL_API = "https://api.github.com/graphql"

headers = {
    "Authorization": f"Bearer {GITHUB_API_KEY}",
    "Content-Type": "application/json"
}

def create_project_field(projectId):
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
        'dataType': 'NUMBER',  # You can change the type if needed
        'name': 'Time Estimate',  # Field name
        'projectId': projectId,  # Project ID
    }
    
    payload = {
        'query': query_create_project_field,
        'variables': variables
    }
    
    try:
        response = requests.post(GITHUB_GRAPHQL_API, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        if "errors" in data:
            print("Errors:", data["errors"])
            return None
        
        project_field = data["data"]["createProjectV2Field"]["projectV2Field"]
        return project_field
        
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None


# Example usage:
project_id = "PVT_kwHOBWsYlM4Athd3"
result = create_project_field(project_id)
if result:
    print(f"Field ID: {result}")