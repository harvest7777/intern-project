from uagents import Model, Field
from datetime import datetime

class YOUR_MODEL(Model):
    attr1: float = Field(
        ...,
        description="blah blah blah"
    )
    attr2: float = Field(
        ...,
        description="blah blah blah"
    )