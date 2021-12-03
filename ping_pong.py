from random import randint
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

ENDPOINT_PARTNERS = {
    'b': "http://localhost:8000/a/",
    'a': "http://localhost:8000/b/"
}


class Payload(BaseModel):
    name: str = "payload"
    digits: list[int] = Field(default_factory=list)
    avg: Optional[int] = None
    max: Optional[int] = None
    min: Optional[int] = None


async def make_post(url: str, payload: any) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload.dict())
    return response


def is_valid() -> bool:
    r = randint(0, 10)
    return False if r % 3 == 0 else True


def validate(payload):
    if not is_valid():
        raise HTTPException(status_code=400, detail=f'Bad Request, payload = {payload}')


def a_processor(payload: Payload):
    payload.digits.append(randint(0, 100))
    return payload


def b_processor(payload: Payload):
    d = payload.digits
    payload.avg = sum(d) / len(d)
    payload.max = max(d)
    payload.min = min(d)
    return payload


def make_routes(endpoint_route: str, app: APIRouter, process: callable) -> None:
    """
    Creates fastapi route(s)
    :param endpoint_route: string ['a' | 'b']
    :param app: APIRouter fastapi app
    :param process: payload processing function
    :return: None
    """

    @app.post(f"/{endpoint_route}/")
    async def act(payload: Payload) -> str:
        """
        fastapi service: validates json payload, processes payload and POSTs it to partner fastapi service if valid,
                otherwise raises 400
        :param payload: jsonified Payload instance
        :return: httpx.Response
        """
        validate(payload)
        process(payload)
        response = await make_post(ENDPOINT_PARTNERS[endpoint_route], payload)
        return f"{response}"
