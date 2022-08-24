import secrets
import time
from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger
from Data.models import *


def generate_name_by_data() -> str:
    return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())


class TaskUnit:
    id: str
    name: str
    create_time: float
    command: str
    scheduler_job: Job
    crontab_exp: str

    def __init__(self, task_command: str, *, task_name: str = None, task_id: str = None, crontab_exp: str = None, create_time: float = None) -> None:
        self.command = task_command
        self.id = task_id if task_id else secrets.token_hex(8)
        self.name = task_name if task_name else generate_name_by_data()
        self.crontab_exp = crontab_exp
        self.create_time = create_time if create_time else time.time()

    @staticmethod
    def create_by_task_info(task_info: TaskInfo) -> 'TaskUnit':
        task = TaskUnit(task_info.command, task_name=task_info.name,
                        task_id=task_info.id, create_time=task_info.create_time, crontab_exp=task_info.crontab_exp)
        if task.crontab_exp:
            task.scheduler_job = CronTrigger(task.crontab_exp)
        return task
