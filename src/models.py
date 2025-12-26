from datetime import datetime

from pydantic import BaseModel, Field, field_validator

class TextEntity(BaseModel):
    type: str
    text: str



class Message(BaseModel):
    id: int
    type: str
    date: datetime
    from_user: str | None = Field(None, alias="from")
    text: str | list # text can be a list (if it contains formatting/links)
    text_entities: list = []

    @field_validator('date', mode='before')
    def parse_date(cls, v):
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S") # adjust format if needed



        return v
    
    @property
    def clean_text(self) -> str:
        if isinstance(self.text, list):
            # telegram sometimes splits text with links/formatting into a list
            parts = []
            for item in self.text:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and 'text' in item:
                    parts.append(item['text'])
            return "".join(parts)
        return str(self.text) if self.text is not None else ""

class ChatExport(BaseModel):
    name: str
    type: str
    id: int
    messages: list[Message]
