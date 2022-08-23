from typing import *
from Utils import *
import subprocess
import shlex


class ExecuteUnit:
    def __init__(self, command: str) -> None:
        '''
        任务执行单元
        :param session_info:`Session`类, 提供session的信息 
        '''
        assert len(command) > 3
        self.command = shlex.split(command)
        self.task = None
        self.__stdout = None
        self.__stderr = None
        try:
            self.task = subprocess.Popen(
                self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as oserr:
            logger.error(oserr)
        except ValueError as valerr:
            logger.error(valerr)
        logger.info('INFO:      Start execute  => %s', self.command)

    def finished(self) -> bool:
        return self.task and self.task.poll() is not None

    def kill(self):
        if self.task:
            self.task.kill()

    def wait(self, timeout=None):
        self.task.wait(timeout)

    @property
    def stdout(self) -> str:
        if self.__stdout:
            return self.__stdout
        if self.task is None:
            return ''
        if not self.finished():
            logger.warning("attempt to access not finished process")
            return ''
        self.__stdout = autoDecode(self.task.stdout.read())
        return self.__stdout

    @property
    def stderr(self) -> str:
        if self.__stderr:
            return self.__stderr
        if self.task is None:
            return ''
        if not self.finished():
            logger.warning("attempt to access not finished process")
            return ''
        self.__stderr = autoDecode(self.task.stderr.read())
        return self.__stderr
