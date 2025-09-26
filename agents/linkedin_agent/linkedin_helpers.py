
def get_linkedin_auth_url(composio, user_id: str):
    connection_request = composio.connected_accounts.link(user_id, "ac_S29IN2PEi_IR")

    redirect_url = connection_request.redirect_url
    return redirect_url

def get_linkedin_urn(composio, user_id: str) -> str | None:
    # LinkedIn post tool
    tool_slug = "LINKEDIN_GET_MY_INFO"
    input_payload = {}

    try:
        # Call the LinkedIn post tool
        response = composio.tools.execute(
            slug=tool_slug,
            arguments=input_payload,
            user_id=user_id
        )
        urn = response["data"]["response_dict"]["author_id"]
        return urn
    except Exception as e:
        print(f"Error fetching LinkedIn URN: {e}")
        # Either the user isn't linked, or LinkedIn didn't return expected data
        return None

def post_to_linkedin(composio, user_id: str, urn: str, content: str) -> dict:
    # LinkedIn post tool
    tool_slug = "LINKEDIN_GET_MY_INFO"

    # Post content
    input_payload = {
        "author": urn,
        "commentary": content,
        "lifecycleState": "PUBLISHED",
        "visibility": "PUBLIC"
    }

    tool_slug = "LINKEDIN_CREATE_LINKED_IN_POST"
    try:
        response = composio.tools.execute(
            slug=tool_slug,
            arguments=input_payload,
            user_id=user_id
        )
    except Exception as e:
        print(f"Error posting to LinkedIn: {e}")
        response = {"success": False, "error": str(e)}

    return response["data"]["response_data"] 

if __name__ == "__main__":
    import os
    from composio import Composio
    from dotenv import load_dotenv
    load_dotenv()
    COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")

    if COMPOSIO_API_KEY is None:
        raise ValueError("Missing required environment variable: COMPOSIO_API_KEY")

    composio = Composio(api_key=COMPOSIO_API_KEY)
    # print(get_linkedin_urn(composio, "user-1349-129-12"))
    share_id = "ilasjfilasjfil"
    response = f"✅ Successfully posted to LinkedIn!  \n+-------+  \n| (•‿•) | --> [View Post Here](https://www.linkedin.com/feed/update/urn:li:share:{share_id}/)  \n+-------+  \n\n[ in ]"
    print(response)