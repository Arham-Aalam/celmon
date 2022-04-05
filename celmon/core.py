import json
import os, sys, json
import importlib

import django
from rich.console import Console
from rich.table import Table

from celery import Celery

from .models import QueueItem, Task

class Celmon(object):

    def __init__(self, celery_app: Celery) -> None:
        self.celery_app = celery_app
    
    def __init__(self, app_name: str) -> None:
        self.app = app_name
        self.context = self._get_app_context()

    def _get_app_context(self) -> None:
        script_path = os.path.join(os.path.abspath('..'), self.app)
        sys.path.append(script_path)
        os.environ['DJANGO_SETTINGS_MODULE'] = f'{self.app}.settings'
        django.setup()
        try:
            self.celery_app = importlib.import_module('from {self.app}.celery import app as celery_app')
        except:
            raise ImportError(f'{self.app} does not have celery setup!')

    '''
    validate if it is a queue containing tasks
    '''
    def _is_queue(self, value: list) -> bool:
        if len(value) == 0:
            return True
        
        try:
            sample = value[0]
            sample = sample.decode('utf-8')
            sample = json.loads(sample)

            return 'headers' in sample or 'body' in sample
        except:
            return False
        return True

    '''
    Get queue len
    '''
    def get_queue_len(self, key, conn=None) -> int:
        if conn is None:
            conn = self.celery_app.pool.acquire(block=True)
        
        return conn.default_channel.client.llen(key)

    '''
    Get all the queues
    '''
    def get_queues(self, conn=None) -> list:
        if conn is None:
            conn = self.celery_app.pool.acquire(block=True)
        
        keys = conn.default_channel.client.keys('*')
        
        # Filter by list type
        queues = []
        for key in keys:
            if conn.default_channel.client.type(key) == 'list':
                queues.append(key)
        
        # TODO: Also filter by properties

        return queues

    '''
    Listout all the tasks
    '''
    def get_tasks_list(self, conn=None) -> list:
        if conn is None:
            conn = self.celery_app.pool.acquire(block=True)
        
        queues = self.get_queues(conn=conn)
        keys = conn.default_channel.client.keys('*')
        keys = [key for key in keys if key not in queues]

        # TODO: Also filter by properties

        tasks = []
        for key in keys:
            try:
                task = Task(conn.default_channel.client.get(key))
            except Exception as e:
                print("[INFO] not a valid JSON", e)
                continue

            if 'task_id' in task.data:
                tasks.append(task)
        
        return tasks

    def get_queue_items(self, key, conn=None):
        if conn is None:
            conn = self.celery_app.pool.acquire(block=True)
        
        qlen = self.get_queue_len(key, conn=conn)
        items = conn.default_channel.client.lrange(key, 0, qlen+1)

        items_new = []
        for item in items:
            try:
                item = QueueItem(conn.default_channel.client.get(key))
            except Exception as e:
                print("[INFO] not a valid JSON", e)
                continue
            if 'headers' in item.data:
                items_new.append(item)
        
        return items_new


class CelmonCLI(Celmon):

    def __init__(self, app_name: str) -> None:
        super().__init__(app_name)

    def loop(self):
        # Refer: https://rich.readthedocs.io/en/latest/live.html
        pass

    def show_tasks_status(self):
        tasks = self.get_tasks_list()

        # Define table header
        table = Table(title="Celery tasks")
        table.add_column("task_id", justify="left", style="cyan", no_wrap=True)
        table.add_column("status", style="red")
        table.add_column("date_done", justify="left", style="green")
        table.add_column("result", justify="left", style="green")

        for task in tasks:
            table.add_row(task.data.get('task_id', 'NA'), 
                task.data.get('status', 'NA'), 
                task.data.get('date_done', 'NA'),
                task.data.get('result', 'NA'))

        console = Console()
        console.print(table)

    def show_queues(self):
        queues = self.get_queues()
        qlens = []

        for queue in queues:
            qlens.append(self.get_queue_len(queue))

        table = Table(title="Celery queues")
        table.add_column("queue", justify="left", style="cyan", no_wrap=True)
        table.add_column("number of tasks", style="green")

        for queue, qlen in zip(queues, qlens):
            table.add_row(queue, qlen)

        console = Console()
        console.print(table)
