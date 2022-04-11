from typing import *
from utils import *
import subprocess
import shlex


class ExecuteUnit:
    def __init__(self, session_info: SessionInfo) -> None:
        '''
        任务执行单元
        :param session_info:`SessionInfo`类, 提供session的信息 
        '''
        self.session_info = session_info
        self.command = shlex.split(session_info.session_command)
        self.task = subprocess.Popen(
            self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        pass

    def finished(self) -> bool:
        return self.task.poll() is not None

    def kill(self):
        self.task.kill()

    @property
    def stdout(self) -> str:
        return self.task.stdout.read().decode()

    @property
    def stderr(self) -> str:
        return self.task.stderr.read().decode()
