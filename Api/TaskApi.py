from Data import dataManager
from Data.models import SessionInfo, TaskInfo
from fastapi import APIRouter
from TaskCore import taskManager

from .models import SessionQueryForm, TaskUploadForm, TaskQueryForm
from .utils import *

from typing import List
taskapi = APIRouter(prefix='/task')


@taskapi.post('/addtask')
@catch_error
@require_token
async def add_task(form: TaskUploadForm):
    taskManager.add_task(form.command, form.crontab_exp, form.name)
    return make_response(CodeResponse.SUCCESS)


@taskapi.post('/getsessioninfo')
@catch_error
@require_token
async def get_session_info(form: SessionQueryForm):
    res_list: List[SessionInfo] = []
    with dataManager.get_session() as sess:
        for sess_id in form.session_id:
            res = sess.query(SessionInfo).filter(SessionInfo.id == sess_id)
            sess_info = res.first()
            if sess_info:
                res_list.append(sess_info)
    return make_response(CodeResponse.SUCCESS, {'result': res_list})


@taskapi.post('/gettaskinfo')
@catch_error
@require_token
async def get_task_info(form: TaskQueryForm):
    res_list: List[TaskInfo] = []
    with dataManager.session as sess:
        for task_id in form.task_id:
            res = sess.query(TaskInfo).filter(TaskInfo.id == task_id)
            if form.require_active:
                res = res.filter(TaskInfo.active == True)
            task_info = res.first()
            if task_info:
                res_list.append(task_info)
    return make_response(CodeResponse.SUCCESS, {'result': res_list})
