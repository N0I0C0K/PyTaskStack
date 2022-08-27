from Data import dataManager
from Data.models import TaskInfo
from fastapi import APIRouter
from TaskCore import taskManager

from .models import TaskDelForm, TaskUploadForm, TaskQueryForm
from .utils import *

from typing import List
taskapi = APIRouter(prefix='/task')


@taskapi.post('/add')
@catch_error
@require_token
async def add_task(form: TaskUploadForm):
    taskManager.add_cron_task(form.command, form.crontab_exp, form.name)
    return make_response(CodeResponse.SUCCESS)


@taskapi.post('/get')
@catch_error
@require_token
async def get_task_info(form: TaskQueryForm):
    res_list: List[TaskInfo] = None
    with dataManager.session as sess:
        if len(form.task_id) > 0:
            res = sess.query(TaskInfo).filter(TaskInfo.id.in_(form.task_id))
        else:
            res = sess.query(TaskInfo)
        if form.require_active:
            res = res.filter(TaskInfo.active == True)
        res_list = res.all()
    return make_response(CodeResponse.SUCCESS, {'result': res_list})


@taskapi.post('/del')
@catch_error
@require_token
async def del_task(form: TaskDelForm):
    with dataManager.session as sess:
        res = sess.query(TaskInfo).filter(TaskInfo.id.in_(form.task_id))
        nums = res.delete()
    return make_response(CodeResponse.SUCCESS, {'del_nums': nums})


@taskapi.post('/stop')
@catch_error
@require_token
async def stop_task(form: TaskQueryForm):
    for task_id in form:
        taskManager.stop_task_by_id(task_id)
