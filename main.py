import uvicorn
from fastapi import FastAPI

from Api.TaskApi import taskapi
from Api.SessionApi import sessionapi
from Api.UserAuthApi import user_auth_api

from TaskCore import taskManager
from Auth import auth_manager
import asyncio

DEBUG = True

if DEBUG:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(taskapi)
app.include_router(sessionapi)
app.include_router(user_auth_api)


def main_func():
    from uvicorn import Config, Server
    main_loop = asyncio.new_event_loop()
    config = Config(app, '0.0.0.0', 5555, loop=main_loop)
    server = Server(config=config)
    taskManager.start(main_loop)
    auth_manager.start_check_token_process(main_loop)
    main_loop.run_until_complete(server.serve())


if __name__ == '__main__':
    main_func()
