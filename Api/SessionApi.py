from Data import dataManager
from Data.models import SessionInfo
from fastapi import APIRouter

from .models import SessionQueryForm, SessionQueryByTaskForm, SessionDelForm
from .utils import *

from typing import List, Dict
sessionapi = APIRouter(prefix='/session')


@sessionapi.post('/getfromid')
@catch_error
@require_token
async def get_session_info_by_id(form: SessionQueryForm):
    res_list: List[SessionInfo] = None
    with dataManager.get_session() as sess:
        if len(form.session_id) > 0:
            res = sess.query(SessionInfo).filter(
                SessionInfo.id.in_(form.session_id))
        else:
            res = sess.query(SessionInfo)
        res_list = res.all()
    return make_response(CodeResponse.SUCCESS, {'result': res_list})


@sessionapi.post('/getfromtask')
@catch_error
@require_token
async def get_session_info_by_task(form: SessionQueryByTaskForm):
    res_dict: Dict[str, List[SessionInfo]] = dict()
    with dataManager.session as sess:
        for task_id in form.task_id:
            res = sess.query(SessionInfo).filter(
                SessionInfo.task_id == task_id)
            res_dict[task_id] = res.all()
    return make_response(CodeResponse.SUCCESS, {'result': res_dict})


@sessionapi.post('/del')
@catch_error
@require_token
async def del_session(form: SessionDelForm):
    with dataManager.session as sess:
        res = sess.query(SessionInfo).filter(
            SessionInfo.id.in_(form.session_id))
        nums = res.delete()
    return make_response(CodeResponse.SUCCESS, {'del_nums': nums})


@sessionapi.get('/info/{session_id}')
async def get_one_session(session_id: str):
    with dataManager.session as sess:
        res = sess.query(SessionInfo).filter(SessionInfo.id == session_id)
    return make_response(CodeResponse.SUCCESS, {'result': res.first()})
