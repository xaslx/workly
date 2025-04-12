from fastapi import APIRouter, status, Request, HTTPException, Response
from dishka.integrations.fastapi import inject, FromDishka as Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.application.use_cases.auth.login import LoginUserUseCase
from src.domain.user.entity import UserEntity
from src.application.use_cases.auth.register import RegisterUserUseCase
from src.presentation.schemas.code.code import LoginUserWithCode, SendCodeSchema, CheckCodeSchema
from src.application.services.code import SendCode, CheckCode
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
    send_code: SendCodeSchema,
    use_case: Depends[SendCode],
) -> bool:

    res: bool = await use_case.execute(telegram_id=send_code.telegram_id, auth_type=send_code.auth_type)

    if res:
        return True
    return False


@router.post(
    '/verify-code',
    description='Эндпоинт для проверки кода',
    status_code=status.HTTP_200_OK,
)
@inject
async def verify_code(
    code: CheckCodeSchema,
    use_case: Depends[CheckCode]
) -> bool:
    
    res: bool = await use_case.execute(code=code.confirmation_code, telegram_id=code.telegram_id)

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
) -> UserEntity:
    
    user: UserRegisterDTO = UserRegisterDTO(
        telegram_id=new_user.telegram_id,
        name=new_user.name,
        username=new_user.username,
    )
    user: UserEntity = await use_case.execute(new_user=user)
    return user


@router.post(
    '/login',
    description='Эндпоинт для входа',
    status_code=status.HTTP_200_OK,
)
@inject
async def login_user(
    login_schema: LoginUserWithCode,
    response: Response,
    use_case: Depends[LoginUserUseCase],
) -> None:
    
    token: str = await use_case.execute(telegram_id=login_schema.telegram_id, code=login_schema.confirmation_code)
    response.set_cookie(key='user_access_token', value=token, max_age=10, httponly=True)