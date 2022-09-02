from Auth import auth_manager
from fastapi import APIRouter

from .models import UserForm
from .utils import *

user_auth_api = APIRouter(prefix='/user')


@user_auth_api.get('/open_session')
@catch_error
async def get_key(username: str):
    key = auth_manager.open_session(username)
    return make_response(CodeResponse.SUCCESS, {'key': key})


@user_auth_api.get('/getusersalt')
@catch_error
async def get_user_salt(username: str):
    salt = auth_manager.get_user_salt(username)
    return make_response(CodeResponse.SUCCESS, {'salt': salt})


@user_auth_api.post('/register')
async def register(form: UserForm):
    if auth_manager.register(form.username, form.pwd):
        return make_response(CodeResponse.SUCCESS)
    return make_response(CodeResponse.UNKONOW_ERR)


@user_auth_api.post('/login')
@catch_error
async def login(form: UserForm):
    token = auth_manager.login(form.username, form.pwd)
    return make_response(CodeResponse.SUCCESS, {'token': token})
