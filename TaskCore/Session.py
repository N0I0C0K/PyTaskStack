import time
import secrets
from .TaskUnit import TaskUnit
from Utils import logger, format_time
from ExecuteCore.ExecuteUnit import ExecuteUnit
from Data import dataManager
from Data.models import SessionInfo


DEFAULT_TIMEOUT = 60*10


class Session:
    id: str
    invoke_time: float
    finish_time: float = 0
    exectue_unit: ExecuteUnit

    def __init__(self, task: TaskUnit) -> None:
        '''
        每次执行任务都会生成一个session.
        '''
        self.task = task
        self.id = secrets.token_hex(8)
        self.exectue_unit = None
        self.closed = False
        logger.info("start new session, id => %s, task name => %s",
                    self.id, self.task.name)

    def __hash__(self) -> int:
        return hash(self.id)

    def run(self, wait: bool = False, *, timeout=DEFAULT_TIMEOUT):
        self.invoke_time = time.time()
        self.exectue_unit = ExecuteUnit(self.task.command)
        logger.info('session %s start run at %s', self.id,
                    format_time(self.invoke_time))
        self.save()
        if wait:
            try:
                self.exectue_unit.wait(timeout)
            except Exception as err:
                logger.error(err)
                self.exectue_unit.kill()

    def save(self):
        with dataManager.get_session() as sess:
            query = sess.query(SessionInfo).filter(
                SessionInfo.id == self.id)
            tar: SessionInfo = query.first()
            if tar:
                tar.invoke_time = self.invoke_time
                tar.task_id = self.task.id
                tar.std_out = self.exectue_unit.stdout
                tar.std_err = self.exectue_unit.stderr
                tar.command = self.task.command
                tar.finish_time = self.finish_time
            else:
                session_info = SessionInfo(
                    id=self.id,
                    invoke_time=self.invoke_time,
                    task_id=self.task.id,
                    std_out=self.exectue_unit.stdout,
                    std_err=self.exectue_unit.stderr,
                    command=self.task.command,
                    finish_time=self.finish_time)
                sess.add(session_info)
            sess.commit()

    def close(self):
        '''
        关闭一个session, 并且上传数据
        '''
        if self.closed:
            return
        logger.info('session %s completed', self.id)
        self.finish_time = time.time()
        self.closed = True
        self.save()

    @property
    def finished(self) -> bool:
        return self.exectue_unit is not None and self.exectue_unit.finished()

    def __del__(self):
        self.close()

    def __json__(self) -> dict:
        return {'id': self.id, 'invoke_time': self.invoke_time, 'command': self.task.command}
