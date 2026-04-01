from pydantic import BaseModel, Field

class StoryRequest(BaseModel):
    story: str = Field(description="The story to be generated, should not be more than 500 words, should be a friendly tone intened for children", example="Once upon a time, in a land far away..." )
    lesson: str = Field(description="The lesson to be included in the story", example="The importance of kindness")
    age_group: str = Field(description="The age group for which the story is intended", example="3-5 years old")
    