import secrets
import time
from apscheduler.job import Job
from Data import dataManager
from Data.models import *

from typing import Optional


def generate_name_by_data() -> str:
    return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())


class TaskUnit:
    id: str
    name: str
    active: bool = True
    create_time: float
    command: str
    scheduler_job: Job
    crontab_exp: Optional[str]

    __active: bool = True

    def __init__(self, task_command: str, *, task_name: str = None, task_id: str = None, crontab_exp: str = None, create_time: float = None) -> None:
        self.command = task_command
        self.id = task_id if task_id else secrets.token_hex(8)
        self.name = task_name if task_name else generate_name_by_data()
        self.crontab_exp = crontab_exp
        self.create_time = create_time if create_time else time.time()
        self.save()

    def save(self):
        '''
        如果数据库不存在当前task就创建, 否则更新.
        '''
        if dataManager.has_item_by_id(TaskInfo, self.id):
            # TODO 更新操作
            pass
        else:
            with dataManager.get_session() as sess:
                task_info = TaskInfo(id=self.id,
                                     name=self.name,
                                     create_time=self.create_time,
                                     command=self.command,
                                     crontab_exp=self.crontab_exp,
                                     active=self.active)
                sess.add(task_info)
                sess.commit()

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def set_active(self, val: bool):
        if not self.scheduler_job:
            return
        self.__active = val
        if val:
            self.scheduler_job.resume()
        else:
            self.scheduler_job.pause()
        self.scheduler_job.modify

    @staticmethod
    def create_by_task_info(task_info: TaskInfo) -> 'TaskUnit':
        task = TaskUnit(task_info.command, task_name=task_info.name,
                        task_id=task_info.id, create_time=task_info.create_time, crontab_exp=task_info.crontab_exp)
        return task
