import secrets
import typing

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger
from typing import Dict
from .TaskUnit import TaskUnit
from .Session import Session

TaskId = typing.NewType('TaskId', str)
SessionId = typing.NewType('SessionId', str)


class TaskManager:

    def __init__(self) -> None:
        self.scheduler: BlockingScheduler = BlockingScheduler()
        self.tasks: Dict[TaskId, TaskUnit] = dict()
        self.sessions: Dict[SessionId, Session] = dict()

    def add_task(self, task_command, crontab_exp: str, task_name: str = None):
        cronTrigger = CronTrigger.from_crontab(crontab_exp)
        task = TaskUnit(task_command, task_name=task_name,
                        crontab_exp=crontab_exp)
        job = self.scheduler.add_job(
            self.run_task, trigger=cronTrigger, name=task.name, id=task.id, args=(task,))
        task.scheduler_job = job

        self.tasks[task.id] = task

    def run_task(self, task: TaskUnit):
        session = Session(task)
        session.run(True)


taskManager = TaskManager()
'''
任务管理
'''
