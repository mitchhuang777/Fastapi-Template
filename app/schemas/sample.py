from pydantic import BaseModel
from typing import List, Optional

class SampleResponse(BaseModel):
    message: str