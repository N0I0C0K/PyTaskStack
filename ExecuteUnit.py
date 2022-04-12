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
        self.task = None
        self.__stdout = None
        self.__stderr = None
        try:
            self.task = subprocess.Popen(
                self.command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError as oserr:
            logging.error(oserr)
        except ValueError as valerr:
            logging.error(valerr)
        logging.debug('[*] Start execute %s => %s',
                      self.session_info.session_id, self.command)
        pass

    def finished(self) -> bool:
        return self.task and self.task.poll() is not None

    def kill(self):
        if self.task:
            self.task.kill()

    @property
    def stdout(self) -> str:
        if self.__stdout:
            return self.__stdout
        if self.task is None:
            return ''
        self.__stdout = autoDecode(self.task.stdout.read())
        return self.__stdout

    @property
    def stderr(self) -> str:
        if self.__stderr:
            return self.__stderr
        if self.task is None:
            return ''
        self.__stderr = autoDecode(self.task.stderr.read())
        return self.__stderr
