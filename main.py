from fastapi import FastAPI, Request
from pydantic import BaseModel
from SessionCore import sessionManager
from typing import *
import uvicorn
import logging

app = FastAPI()
logging.basicConfig(filename='./log/test.log',
                    level=logging.DEBUG, encoding='utf-8')


class SeeionForm(BaseModel):
    token: str                        # 密钥
    session_id: str                   # session id
    session_name: str                 # 任务名称
    session_command: str              # 任务需要执行的命令
    stdout_log: Optional[str] = None  # 标准输出输出到哪个文件
    stderr_log: Optional[str] = None  # 标准错误输出到哪个文件


@app.get('/')
async def index():
    return {'code': 200, 'msg': 'Welcome to PyTaskStack'}


@app.get('/getsession')
async def get_session(req: Request):
    logging.debug(req.client)
    session_id, key = sessionManager.newSession()
    return {'code': 200, 'session_id': session_id, 'key': key}


@app.post('/pushsession')
async def push_session(form: SeeionForm, req: Request):
    logging.debug(req.client)
    if not sessionManager.verify(form.session_id, form.token):
        return {'code': 500, 'msg': '非法授权'}
    sessionManager.updateSessionInfoByDict(form.session_id, form.dict())
    return {'code': 200}


@app.get('/session/{session_id}')
async def view_session(session_id: str, req: Request):
    logging.debug('%s ==========> %s', session_id, req.client)

    pass


@app.get('/test')
async def test(req: Request):
    print(req.client)
    return req.headers

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5555)
