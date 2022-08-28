import uvicorn
from fastapi import FastAPI

from Api.TaskApi import taskapi
from Api.SessionApi import sessionapi

from TaskCore import taskManager
import asyncio

DEBUG = True

if DEBUG:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(taskapi)
app.include_router(sessionapi)

if __name__ == '__main__':
    taskManager.start()
    uvicorn.run(app, host='0.0.0.0', port=5555)
