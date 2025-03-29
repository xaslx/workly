from fastapi import APIRouter, Request
from dishka.integrations.fastapi import inject, FromDishka as Depends
from fastapi.templating import Jinja2Templates


router: APIRouter = APIRouter()


@router.get('/')
@inject
async def main_page(
    request: Request,
    template: Depends[Jinja2Templates],
):
    return template.TemplateResponse(
        request=request,
        name='base.html',
    )