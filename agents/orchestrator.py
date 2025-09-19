from schemas import *
from addresses import AGENT_ADDRESSES

from datetime import datetime
from uuid import uuid4

import os
from dotenv import load_dotenv
from uagents import Context, Protocol, Agent
from uagents.setup import fund_agent_if_low

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
    name="Orchestrator",
    seed=os.getenv("AGENT_SEED_PHRASE"),
    port=8000,
    endpoint="http://localhost:8000/submit",
)

fund_agent_if_low(str(agent.wallet.address()))
protocol = Protocol(spec=chat_protocol_spec)

@protocol.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.now(), acknowledged_msg_id=msg.msg_id),
    )
    response = "I'm the Orchestrator"
    # is_start_of_chat: AgentContent = isinstance(msg.content[-1], StartSessionContent)
    is_user_message = isinstance(msg.content[-1], TextContent)
    ctx.logger.info(msg)
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

@agent.on_interval(5)
async def handle_get_weather(ctx: Context):
    ctx.logger.info("Trying to query weather agent")
    await ctx.send(AGENT_ADDRESSES.WEATHER, WeatherQuery(latitude=34.0522, longitude=-118.2437))

@agent.on_message(model=WeatherResponse)
async def handle_weather_response(ctx: Context, sender: str, msg: WeatherResponse):
    ctx.logger.info(f"Received weather response: {msg}")

@protocol.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    pass

# I believe you have to have this to register it to AgentVerse
agent.include(protocol, publish_manifest=True)
if __name__ == "__main__":
    agent.run()