from pydantic import BaseModel

class ReqModel(BaseModel):
    input_text: str
    entity_types: dict[str, str] | list[str] | None = None