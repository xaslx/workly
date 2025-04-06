from fastapi import APIRouter, status, Request, HTTPException
from dishka.integrations.fastapi import inject, FromDishka as Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.application.use_cases.user.register import RegisterUserUseCase
from src.presentation.schemas.code.code import SendCodeSchema, CheckCodeSchema
from src.application.use_cases.code.code import SendCode, CheckCode
from src.application.dto.user.register import UserRegisterDTO
from src.presentation.schemas.user.register import RegisterUserSchema



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


@router.post(
    '/send-code',
    description='Эндпоинт для отправки кода',
    status_code=status.HTTP_200_OK,
)
@inject
async def send_code(
    telegram_id: SendCodeSchema,
    use_case: Depends[SendCode],
):
    print(f'TG ID: {telegram_id}')
    res: bool = await use_case.execute(telegram_id=telegram_id.telegram_id)
    if res:
        return True


@router.post(
    '/verify-code',
    description='Эндпоинт для проверки кода',
    status_code=status.HTTP_200_OK,
)
@inject
async def verify_code(
    code: CheckCodeSchema,
    use_case: Depends[CheckCode]
):
    res: bool = await use_case.execute(code=code.confirmation_code, telegram_id=code.telegram_id)
    print(res)
    if not res:
        raise HTTPException(status_code=400, detail='Неверный код подтверждения')
    return res 


@router.post(
    '/register',
    description='Эндпоинт для регистрации нового пользователя',
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register_user(
    new_user: RegisterUserSchema,
    use_case: Depends[RegisterUserUseCase]
):
    user: UserRegisterDTO = UserRegisterDTO(
        telegram_id=new_user.telegram_id,
        name=new_user.name,
        username=new_user.username,
    )
    res = await use_case.execute(new_user=user)
    print(res)