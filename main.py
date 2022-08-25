import uvicorn
from fastapi import FastAPI

from Api.TaskApi import taskapi

from TaskCore import taskManager

DEBUG = True

if DEBUG:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(taskapi)

if __name__ == '__main__':
    taskManager.start()
    uvicorn.run(app, host='0.0.0.0', port=5555)
