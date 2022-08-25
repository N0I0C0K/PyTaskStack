import typing
from typing import Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from Data import dataManager
from Data.models import TaskInfo
from sqlalchemy import select
from Utils import logger

from .Session import Session
from .TaskUnit import TaskUnit


TaskId = typing.NewType('TaskId', str)
SessionId = typing.NewType('SessionId', str)


class TaskManager:

    def __init__(self) -> None:
        self.scheduler: BackgroundScheduler = BackgroundScheduler()
        self.scheduler.modify_job
        self.tasks: Dict[TaskId, TaskUnit] = dict()
        self.sessions: Dict[SessionId, Session] = dict()

    def load_task_from_database(self):
        logger.info('start load task from database')
        with dataManager.get_session() as sess:
            stmt = select(TaskInfo)
            task: TaskInfo
            for task in sess.scalars(stmt):
                logger.info('load %s: %s', task.id, task.name)
                if task.crontab_exp is not None:
                    task_unit = TaskUnit.create_by_task_info(task)
                    cronTrigger = CronTrigger.from_crontab(
                        task_unit.crontab_exp)
                    job = self.scheduler.add_job(
                        self.run_task, trigger=cronTrigger, name=task_unit.name, id=task_unit.id, args=(task_unit,))
                    task_unit.scheduler_job = job
                    self.tasks[task_unit.id] = task_unit

    def add_task(self, task_command, crontab_exp: Optional[str] = None, task_name: Optional[str] = None):
        logger.info('add new task, command: %s', task_command)
        if not crontab_exp:
            # TODO 无cron表达式, 立马执行命令
            return
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
        session.close()
        del session

    def start(self):
        '''
        开始任务自动化
        '''
        logger.info('start scheduler')
        self.scheduler.start()

    def pause(self):
        '''
        暂停整个任务
        '''
        logger.info('pause scheduler')
        self.scheduler.pause()

    def stop_task_by_id(self, task_id: TaskId):
        '''
        暂停一个Task
        '''
        assert task_id in self.tasks
        self.tasks[task_id].scheduler_job.pause()

    def resume_task_by_id(self, task_id: TaskId):
        '''
        重启一个Task
        '''
        assert task_id in self.tasks
        self.tasks[task_id].scheduler_job.resume()


taskManager = TaskManager()
'''
任务管理
'''
