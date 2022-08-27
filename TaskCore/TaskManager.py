import typing
from typing import Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from Data import dataManager
from Data.models import TaskInfo
from Utils import logger

from .Session import Session
from .TaskUnit import TaskUnit


TaskId = typing.NewType('TaskId', str)
SessionId = typing.NewType('SessionId', str)


class TaskManager:

    def __init__(self) -> None:
        self.scheduler: BackgroundScheduler = BackgroundScheduler()
        self.tasks: Dict[TaskId, TaskUnit] = dict()
        self.sessions: Dict[SessionId, Session] = dict()
        self.load_task_from_database()

    def load_task_from_database(self):
        logger.info('start load task from database')
        with dataManager.get_session() as sess:
            stmt = sess.query(TaskInfo)
            task: TaskInfo
            for task in stmt.all():
                logger.info('load task => %s, %s, %s',
                            task.id, task.name, task.command)
                if task.crontab_exp is not None:
                    task_unit = TaskUnit.create_by_task_info(task)
                    cronTrigger = CronTrigger.from_crontab(
                        task_unit.crontab_exp)
                    job = self.scheduler.add_job(
                        self.run_task, trigger=cronTrigger, name=task_unit.name, id=task_unit.id, args=(task_unit,))
                    task_unit.scheduler_job = job
                    self.tasks[task_unit.id] = task_unit

    def add_cron_task(self, task_command, crontab_exp: str, task_name: Optional[str] = None):
        cronTrigger = CronTrigger.from_crontab(crontab_exp)
        task = TaskUnit(task_command, task_name=task_name,
                        crontab_exp=crontab_exp)
        job = self.scheduler.add_job(
            self.run_task, trigger=cronTrigger, name=task.name, id=task.id, args=(task,))
        task.scheduler_job = job
        self.tasks[task.id] = task
        logger.info('add new task, %s-%s: %s',
                    task.name, task.id, task_command)

    def run_temp_task(self, task_command: str) -> SessionId:
        task = TaskUnit(task_command)
        sess = self.run_task(task, False)
        return sess.id

    def run_task(self, task: TaskUnit, is_sync: bool = True) -> Session:
        session = Session(task)
        session.run(is_sync)
        if is_sync:
            session.close()
            return session
        else:
            return session

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
        self.tasks[task_id].active = False

    def resume_task_by_id(self, task_id: TaskId):
        '''
        重启一个Task
        '''
        assert task_id in self.tasks
        self.tasks[task_id].active = True


taskManager = TaskManager()
'''
任务管理
'''
