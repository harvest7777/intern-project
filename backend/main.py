from composio import Composio

HARDCODED_UUID = "user-1349-129-12"

HARDCODED_API_KEY = "test"
composio = Composio(api_key=HARDCODED_API_KEY)

# Use the "AUTH CONFIG ID" from your dashboard
auth_config_id = "ac_S29IN2PEi_IR"

# Use a unique identifier for each user in your application
user_id = HARDCODED_UUID


def auth():
    connection_request = composio.connected_accounts.link(user_id, auth_config_id, callback_url= 'https://your-app.com/callback')

    redirect_url = connection_request.redirect_url
    print(f"Visit: {redirect_url} to authenticate your account")
                
    # Wait for the connection to be established
    connected_account = connection_request.wait_for_connection()
    print(connected_account.id)

def post():
    # LinkedIn post tool
    tool_slug = "LINKEDIN_GET_MY_INFO"


    input_payload = {}
    # Call the LinkedIn post tool
    response = composio.tools.execute(
        slug=tool_slug,
        arguments=input_payload,
        user_id=user_id
    )
    urn = response["data"]["response_dict"]["author_id"]

    # 🔥 Your manual post content
    input_payload = {
        "author": urn,
        "commentary": "testtsjaklafjaslf",
        "lifecycleState": "PUBLISHED",
        "visibility": "PUBLIC"
    }

    tool_slug = "LINKEDIN_CREATE_LINKED_IN_POST"
    response = composio.tools.execute(
        slug=tool_slug,
        arguments=input_payload,
        user_id=user_id
    )
    print(response)
post()
