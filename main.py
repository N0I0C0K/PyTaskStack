from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from SessionCore import sessionManager
from typing import *
from Utils.utils import *

DEBUG = True

if DEBUG:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5555)
