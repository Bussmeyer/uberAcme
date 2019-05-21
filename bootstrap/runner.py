from dotenv import load_dotenv
load_dotenv()
import os
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint

# Fill in with your personal access token and org URL
personal_access_token = os.getenv("PAT")
organization_url = 'https://dev.azure.com/' + os.getenv("ORG")

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
core_client = connection.clients.get_core_client()

# Get the list of projects in the org
projects = core_client.get_projects()

# Delete all existing projects
for project in projects:
    pprint.pprint(project.__dict__)
    core_client.queue_delete_project(project.id)

projects = {
    "infrastructure",
    "website"
}

for project_name in projects:
    project = {
        "name": project_name,
        "description": "None",
        "visibility": "private",
        "capabilities": {
            "versioncontrol": {
                "sourceControlType": "Git"
            },
            "processTemplate": {
                "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"
            }
        }
    }
    pprint.pprint(project)
    core_client.queue_create_project(project)
