from fastapi import APIRouter, status, Request
from dishka.integrations.fastapi import inject, FromDishka as Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



router: APIRouter = APIRouter()


@router.get(
        '/register',
        description='Эндпоинт для шаблона с регистрацией',
        name='register:page',
        status_code=status.HTTP_200_OK,
)
@inject
async def get_register_template(
    request: Request,
    template: Depends[Jinja2Templates],
) -> HTMLResponse:
    
    return template.TemplateResponse(
        request=request,
        name='register.html',
    )


@router.get(
    '/login',
    description='Эндпоинт для получения шаблона со входом',
    name='login:page',
    status_code=status.HTTP_200_OK,
)
@inject
async def get_login_template(
    request: Request,
    template: Depends[Jinja2Templates],
) -> HTMLResponse:
    
    return template.TemplateResponse(
        request=request,
        name='login.html',
    )