from pydantic import BaseModel

class ReqModel(BaseModel):
    input_text: str
    entity_types: list[str] | None = None