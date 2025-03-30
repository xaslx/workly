from fastapi import FastAPI
from src.presentation.controllers.main import router as main_router
from src.presentation.controllers.auth import router as auth_router


def setup_controllers(app: FastAPI):

    app.include_router(main_router, tags=['Главная страница'])
    app.include_router(auth_router, prefix='/auth', tags=['Регистрация и Вход'])