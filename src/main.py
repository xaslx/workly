from fastapi import FastAPI
from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):

    yield



def create_app() -> FastAPI:

    app: FastAPI = FastAPI(
        title='Workly',
        description='Фриланс биржа',
        lifespan=lifespan,
    )

    return app