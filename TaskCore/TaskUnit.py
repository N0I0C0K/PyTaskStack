import secrets
import time
from typing import Union
from apscheduler.job import Job


def generate_name_by_data() -> str:
    return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())


class TaskUnit:
    id: str
    name: str
    command: str
    scheduler_job: Job
    crontab_exp: str

    def __init__(self, task_command: str, *, task_name: str = None, task_id: str = None, crontab_exp: str = None) -> None:
        self.command = task_command
        self.id = task_id if task_id else secrets.token_hex(8)
        self.name = task_name if task_name else generate_name_by_data()
        self.crontab_exp = crontab_exp
