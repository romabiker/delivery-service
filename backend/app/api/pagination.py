from __future__ import annotations

from typing import Any

from fastapi import Request
from pydantic import BaseModel, Field


class PageNumberPagination(BaseModel):
    items: list[Any] = Field(default_factory=list)
    total: int
    next: str | None = None
    prev: str | None = None


def get_page_number_url(request: Request, page: int, per_page: int, total: int) -> str | None:
    if page * per_page > total or page <= 0:
        return None

    query_params = dict(request.query_params.items())
    query_params["page"] = str(page)
    query_params["per_page"] = str(per_page)

    url = request.url.replace_query_params(**query_params)

    return str(url)


def paginate_by_page_number(
    request: Request, items: list[Any], total: int, page: int, per_page: int
) -> PageNumberPagination:
    return PageNumberPagination(
        items=items,
        total=total,
        next=get_page_number_url(request, page + 1, per_page, total),
        prev=get_page_number_url(request, page - 1, per_page, total),
    )
