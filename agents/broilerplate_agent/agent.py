from models import *
from helpers import *
from datetime import datetime
from uuid import uuid4
import os
from dotenv import load_dotenv
from uagents import Context, Protocol, Agent
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    StartSessionContent,
    EndSessionContent,
    AgentContent,
    TextContent,
    chat_protocol_spec,
)
load_dotenv()

agent = Agent(
    name=YOUR AGENT NAME,
    seed=os.getenv(YOUR AGENT SEED),
    port=8001,
    mailbox=True,
)
protocol = Protocol(spec=chat_protocol_spec)

@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )

    response = "YOUR AGENT RESPONSE"

    is_user_message = isinstance(msg.content[-1], TextContent)

    if is_user_message:
        await ctx.send(sender, ChatMessage(
            timestamp=datetime.now(),
            msg_id=uuid4(),
            content=[
                TextContent(type="text", text=response),

                # This will end the chat session after one interaction
                EndSessionContent(type="end-session") 
            ]
        ))

@agent.on_message(model=YOUR_MODEL)
async def handle_get_weather(ctx: Context, sender: str, msg: YOUR_MODEL):
    ctx.logger.info("Received request")

@agent.on_rest_post(endpoint="/", request=YOUR_MODEL, response=YOUR_MODEL)
async def handle_weather_request(ctx: Context, msg: YOUR_MODEL):
    ctx.logger.info("Received REST request")

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

# I believe you have to have this to register it to AgentVerse
agent.include(protocol, publish_manifest=True)

if __name__ == "__main__":
    agent.run()