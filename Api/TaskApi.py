from fastapi import APIRouter
from .models import TaskForm
from Auth import auth_manager
from .utils import *
from TaskCore import taskManager
taskapi = APIRouter(prefix='/task')


@taskapi.post('/addtask')
async def add_task(form: TaskForm):
    if not auth_manager.verify_token(form.token):
        return make_response(CodeResponse.INVALID_TOKEN)
    taskManager.add_task(form.command, form.crontab_exp, form.name)
