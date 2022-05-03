from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from SessionCore import sessionManager
from typing import *
from utils import *

DEBUG = True

if DEBUG:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.mount('/Web', StaticFiles(directory='Web'), name="static")

templates = Jinja2Templates(directory='Web')


@app.get('/')
async def index():
    return {'code': 200, 'msg': 'Welcome to PyTaskStack'}


@app.get('/getsession')
async def get_session(req: Request):
    '''
    申请`session`的验证阶段
    :return :  ` {'code': 状态码, 'session_id': id}`
    '''
    logging.debug(req.client)
    session_id = sessionManager.newSession()
    return {'code': 200, 'session_id': session_id}


@app.post('/pushsession')
async def push_session(form: FormRaw, req: Request):
    '''
    正式上传`session`的信息
    :return :`{'code':状态码, 'url':session的信息页面url}`
    '''
    logging.debug('%s ==========> %s', req.client, req.base_url.is_secure)
    sessid = sessionManager.updateSessionInfoByRaw(form)
    return {'code': 200, 'url': f'{req.base_url}session/{sessid}'}


@app.get('/session/info/{session_id}')
async def info_session(session_id: str, req: Request):
    '''
    获得`session_id`的执行信息
    '''
    logging.debug('%s ==========> %s', session_id, req.client)
    stdout, stderr = sessionManager.getSessionOutPut(session_id)
    return {'code': 200, 'stdout': stdout, 'stderr': stderr}


@app.get('/session/run/{session_id}')
async def run_session(session_id: str, req: Request):
    '''
    执行`session_id`
    '''
    sessionManager.runSession(session_id)
    return {'code': 200}


@app.get('/session/{session_id}')
async def view_session(session_id: str, req: Request):
    session = sessionManager.getSessionInfo(session_id)
    if session is None:
        return {'code': 404}
    return templates.TemplateResponse('session.html', {'request': req, 'name': session.session_name, 'stdout': session.stdout_log, 'stderr': session.stderr_log})


@app.get('/test')
async def test(req: Request):
    print(req.client)
    return req.headers

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5555)
