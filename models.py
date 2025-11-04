from pydantic import BaseModel, Field

'''
Represents a single to do item.
'''
class TodoItem(BaseModel):
    text: str = Field(description="The text description of the to do item", min_length=1)
    completed: bool = Field(description="Whether or not the item is completed", default=False)