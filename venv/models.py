# Import the BaseModel class from the pydantic module
from pydantic import BaseModel

# Import the Optional type from the typing module
from typing import Optional

# Define a class Task that inherits from Pydantic's BaseModel
class Task(BaseModel):
    # Define a required field 'title' which must be a string
    title: str
    
    # Define an optional field 'description' which is a string, defaulting to None if not provided
    description: Optional[str] = None
    
    # Define a boolean field 'completed' with a default value of False
    completed: bool = False
