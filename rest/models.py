from pydantic import BaseModel, HttpUrl
from typing import Optional

class Term(BaseModel):
    title: str
    definition: str
    source_link: Optional[HttpUrl] = None  # Можно использовать HttpUrl для валидации ссылок

class TermUpdate(BaseModel):
    definition: str
    source_link: Optional[HttpUrl] = None  # Также проверяем, что ссылка валидная
