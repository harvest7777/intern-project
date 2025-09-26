import composio
from linkedin_models import *
from linkedin_helpers import *
from datetime import datetime
from pprint import pformat
from uuid import uuid4
import os
from dotenv import load_dotenv
from uagents import Context, Protocol, Agent
from composio import Composio
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    StartSessionContent,
    EndSessionContent,
    AgentContent,
    MetadataContent,
    TextContent,
    chat_protocol_spec,
)
load_dotenv()
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")

if COMPOSIO_API_KEY is None:
    raise ValueError("Missing required environment variable: COMPOSIO_API_KEY")

composio = Composio(api_key=COMPOSIO_API_KEY)

agent = Agent(
    name="LinkedIn Warrior",
    seed=os.getenv("LINKEDIN_AGENT_SEED"),
    port=8001,
    mailbox=True,
)
protocol = Protocol(spec=chat_protocol_spec)

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

# Every message will have to go through this
@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage, receiver: str | None = None):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    linkedin_urn = get_linkedin_urn(composio, "user-1349-129-12")
    linkedin_is_connected = linkedin_urn is not None
    if linkedin_is_connected:
        post_data = post_to_linkedin(composio, "user-1349-129-12", linkedin_urn, "This was posted using Fetch.ai ASI1 via LinkedIn Agent 😳")
        share_id = post_data.get("share_id", "unknown")
        response = f"☑️ Successfully posted to LinkedIn!  \n(•‿•) [View Post Here](https://www.linkedin.com/feed/update/{share_id}/)"
    else:
        login_url = get_linkedin_auth_url(composio, "user-1349-129-12")
        response = f"Please authenticate your LinkedIn account by visiting: [LinkedIn]({login_url})"

    # Simple broilerplate check to see who the message came from
    # is_user_message = isinstance(msg.content[-1], TextContent)

    is_asi1_message = isinstance(msg.content[-1], MetadataContent)

    formatted_str = "\n" + pformat(msg.content[-1].dict(), width=60, indent=2, sort_dicts=False)

    ctx.logger.info(formatted_str)


    if is_asi1_message:
        ctx.logger.info(f"Received message from {sender}")

        await ctx.send(sender, ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response),
                # This will end the chat session after one interaction
                # EndSessionContent(type="end-session") 
            ]
        ))

# TODO: make sure to test this
@agent.on_message(model=LinkedInIsConnectedRequest,replies=LinkedInIsConnectedResponse)
async def handle_linkedin_connection(ctx: Context, sender: str, msg: LinkedInIsConnectedRequest):
    ctx.logger.info("Received request to check LinkedIn connection")
    linkedin_urn = get_linkedin_urn(composio, msg.user_id)
    is_connected = linkedin_urn is not None
    return LinkedInIsConnectedResponse(is_connected=is_connected)

# TODO: make sure to test this
@agent.on_message(model=PostToLinkedInRequest, replies=PostToLinkedInResponse)
async def handle_linkedin_post(ctx: Context, sender: str, msg: PostToLinkedInRequest):
    ctx.logger.info("Received request to post to LinkedIn")
    response = post_to_linkedin(composio=composio, user_id=msg.user_id, urn=msg.urn, content=msg.content)
    return PostToLinkedInResponse(success=response.get("success", False))



# @agent.on_rest_post(endpoint="/", request=YOUR_MODEL, response=YOUR_MODEL)
# async def handle_weather_request(ctx: Context, msg: YOUR_MODEL):
#     ctx.logger.info("Received REST request")


# I believe you have to have this to register it to AgentVerse
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()