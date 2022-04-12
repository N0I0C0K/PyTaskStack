from fastapi import FastAPI, Request
from SessionCore import sessionManager
from typing import *
import uvicorn
from utils import *

app = FastAPI()


@app.get('/')
async def index():
    return {'code': 200, 'msg': 'Welcome to PyTaskStack'}


@app.get('/getsession')
async def get_session(req: Request):
    logging.debug(req.client)
    session_id, key = sessionManager.newSession()
    return {'code': 200, 'session_id': session_id, 'key': key}


@app.post('/pushsession')
async def push_session(form: SessionForm, req: Request):
    logging.debug('%s ==========> %s', req.client, req.base_url.is_secure)
    if not sessionManager.verify(form.session_id, form.token):
        return {'code': 500, 'msg': '非法授权'}
    sessionManager.updateSessionFromForm(form.session_id, form)
    return {'code': 200, 'url': f'{req.base_url}session/{form.session_id}'}


@app.get('/session/{session_id}')
async def view_session(session_id: str, req: Request):
    logging.debug('%s ==========> %s', session_id, req.client)
    stdout, stderr = sessionManager.getSessionOutPut(session_id)
    return {'code': 200, 'stdout': stdout, 'stderr': stderr}


@app.get('/run/{session_id}')
async def run_session(session_id: str, req: Request):
    sessionManager.runSession(session_id)
    return {'code': 200}


@app.get('/test')
async def test(req: Request):
    print(req.client)
    return req.headers

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5555)
