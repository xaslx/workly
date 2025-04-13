from fastapi import APIRouter, Request, status
from dishka.integrations.fastapi import inject, FromDishka as Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.domain.user.entity import UserEntity


router: APIRouter = APIRouter()


@router.get(
        '/',
        description='Эндпоинт для шаблона с главной страницей',
        status_code=status.HTTP_200_OK,
        name='main:page'
)
@inject
async def main_page(
    request: Request,
    template: Depends[Jinja2Templates],
    user: Depends[UserEntity],
) -> HTMLResponse:

    return template.TemplateResponse(
        request=request,
        name='base.html',
        context={'user': user}
    )