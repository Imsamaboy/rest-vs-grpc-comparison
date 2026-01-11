from fastapi import FastAPI, HTTPException
from typing import Dict

from .models import Term, TermUpdate
from .data import data

app = FastAPI()


@app.get("/", response_model=Dict[str, Term])
async def get_terms() -> Dict[str, Term]:
    """
    Получить список всех терминов.
    """
    return data


@app.post("/term/{term_key}", response_model=Term)
async def add_term(term_key: str, term: Term) -> Term:
    """
    Добавить новый термин с описанием.
    """
    if term_key in data:
        raise HTTPException(
            status_code=400,
            detail=f"Термин '{term_key}' уже существует."
        )

    data[term_key] = term
    return term


@app.put("/term/{term_key}", response_model=Term)
async def modify_term(term_key: str, term_update: TermUpdate) -> Term:
    """
    Обновить существующий термин.
    Можно изменить только definition и source_link, но не title.
    """
    existing_term = data.get(term_key)
    if not existing_term:
        raise HTTPException(
            status_code=404,
            detail=f"Термин '{term_key}' не найден."
        )

    existing_term.definition = term_update.definition
    existing_term.source_link = term_update.source_link

    return existing_term
