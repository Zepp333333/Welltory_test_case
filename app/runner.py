import uvicorn
from fastapi import FastAPI, APIRouter
from app.ping_pong import make_routes, a_processor, b_processor


def run():
    service_a = APIRouter()
    service_b = APIRouter()
    make_routes('a', service_a, a_processor)
    make_routes('b', service_b, b_processor)

    app = FastAPI()

    app.include_router(service_a)
    app.include_router(service_b)

    return app


if __name__ == '__main__':
    uvicorn.run("runner:run", reload=True)
