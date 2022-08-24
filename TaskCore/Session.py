import time
import secrets
from .TaskUnit import TaskUnit
from Utils import logger
from ExecuteCore.ExecuteUnit import ExecuteUnit
from Data import dataManager


class Session:
    id: str
    invoke_time: float
    exectue_unit: ExecuteUnit

    def __init__(self, task: TaskUnit) -> None:
        '''
        每次执行任务都会生成一个session.
        '''
        self.task = task
        self.id = secrets.token_hex(8)
        self.exectue_unit = None
        logger.info("start new session, id => %s, task name => %s",
                    self.id, self.task.name)

    def run(self, wait: bool = False, *, timeout=None):
        self.invoke_time = time.time()
        self.exectue_unit = ExecuteUnit(self.task.command)
        if wait:
            self.exectue_unit.wait(timeout)

    def close(self):
        pass
