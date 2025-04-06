from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from dishka.integrations import fastapi as fastapi_integration
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.presentation.controllers.setup_routers import setup_controllers
from src.config import Config
from dishka import AsyncContainer, make_async_container
from src.ioc import AppProvider
from src.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('Приложение запущено')
    yield



def create_app() -> FastAPI:

    config: Config = Config()
    container: AsyncContainer = make_async_container(AppProvider(), context={Config: config})

    app: FastAPI = FastAPI(
        title='Workly',
        description='Фриланс биржа',
        lifespan=lifespan,
    )

    app.mount('/static', StaticFiles(directory='src/presentation/static'), name='static')
    setup_controllers(app=app)
    fastapi_integration.setup_dishka(container=container, app=app)
    
    @app.exception_handler(404)
    async def custom_404_handler(request: Request, __) -> HTMLResponse:
        return RedirectResponse('/')

    return app