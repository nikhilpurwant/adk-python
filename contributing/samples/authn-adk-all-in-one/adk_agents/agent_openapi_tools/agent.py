from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.tools.openapi_tool.auth.auth_helpers import openid_url_to_scheme_credential
import os


credential_dict={"client_id":os.environ.get("OAUTH_CLIENT_ID"),"client_secret":os.environ.get("OAUTH_CLIENT_SECRET")}
auth_scheme, auth_credential = openid_url_to_scheme_credential(openid_url="http://localhost:5000/.well-known/openid-configuration",credential_dict=credential_dict,scopes=[])


# Open API spec
file_path = './agent_openapi_tools/openapi.yaml'
file_content = None

try:
    with open(file_path, 'r') as file:
        file_content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")


# Example with a JSON string
openapi_spec_yaml = file_content # Your OpenAPI YAML string
openapi_toolset = OpenAPIToolset(spec_str=openapi_spec_yaml, spec_str_type="yaml", auth_scheme=auth_scheme,auth_credential=auth_credential)

from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="hotel_agent",
    instruction="Help user find and book hotels, fetch their bookings using the tools provided.",
    description="Hotel Booking Agent",
    model=os.environ.get("GOOGLE_MODEL"),
    tools=[openapi_toolset], # Pass the toolset
    # ... other agent config ...
)