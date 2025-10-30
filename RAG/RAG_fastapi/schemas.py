from typing import Annotated, Literal, TypeAlias
from uuid import uuid4
import tiktoken
from loguru import logger
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    IPvAnyAddress,
    HttpUrl,
)

SupportedTextModels: TypeAlias = Literal["gpt-3.5", "gpt-4"]
TokenCount = Annotated[int, Field(ge=0)]

def count_tokens(text: str | None) -> int:
    if text is None:
        logger.warning("Response is None. Assuming 0 tokens used")
        return 0
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(text))


class ModelResponse(BaseModel):
    request_id: Annotated[str, Field(default_factory=lambda: uuid4().hex)]
    # no defaults set for ip field
    # raise ValidationError if a valid IP address or None is not provided.
    ip: Annotated[str, IPvAnyAddress] | None
    content: Annotated[str | None, Field(min_length=0, max_length=10000)]
    created_at: datetime = datetime.now()


class TextModelRequest(BaseModel):
    model: Literal["gpt-3.5-turbo", "gpt-4o"]
    prompt: str
    temperature: float = 0.0


class TextModelResponse(ModelResponse):
    model: SupportedTextModels
    temperature: Annotated[float, Field(ge=0.0, le=1.0, default=0.0)]
    price: Annotated[float, Field(ge=0, default=0.0)]

    @property
    @computed_field
    def tokens(self) -> TokenCount:
        return count_tokens(self.content)

    @property
    @computed_field
    def cost(self) -> float:
        return self.price * self.tokens