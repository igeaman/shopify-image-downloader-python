from pydantic import BaseModel, Field


class URI(BaseModel):
    URL: str = Field(...)


class Images(BaseModel):
    Images: list[URI]

class description(BaseModel):
    description: str = Field(...)

class title(BaseModel):
    title: str = Field(...)

# request response will be Images, Description, Title
class requestResponse(Images, description, title):
    pass