from uagents import Model, Field
from datetime import datetime

class LinkedInIsConnectedRequest(Model):
    user_id: str = Field(
        ...,
        description="The unique identifier for the user shared across ASI1, Supabase, and Composio"
    )

class LinkedInIsConnectedResponse(Model):
    is_connected: bool = Field(
        ...,
        description="Indicates whether the user is connected to LinkedIn via Composio"
    )


class PostToLinkedInRequest(Model):
    user_id: str = Field(
        ...,
        description="The unique identifier for the user shared across ASI1, Supabase, and Composio"
    )
    urn: str = Field(
        ...,
        description="The LinkedIn URN of the user"
    )
    content: str = Field(
        ...,
        description="The content to post on LinkedIn"
    )

class PostToLinkedInResponse(Model):
    success: bool = Field(
        ...,
        description="Indicates whether the post was successful"
    )