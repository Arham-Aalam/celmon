import json
import os, sys, json
import importlib

import django
from rich.console import Console
from rich.table import Table
from celery.exceptions import DuplicateNodenameWarning
from celery import Celery

from .models import NodeItem, Task, PendingTask

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
            self.celery_app = importlib.import_module(f'{self.app}.celery').app
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
    def get_queue_len(self, node_name, queue=None) -> int:
        nodes = self.celery_app.control.inspect().active()
        node = nodes.get(node_name, [])

        if queue is None:
            return len(node)
        
        count = 0
        for task in node:
            if task.get('delivery_info', {}).get('routing_key', '') == queue:
                count += 1

        return count

    '''
    Get all the queues
    '''
    def get_queues(self) -> list:
        try:
            queues = self.celery_app.control.inspect().active_queues()
        except DuplicateNodenameWarning as e:
            print(e)
            print("[WAR] hint: Make sure you run workers with different node names.")
            queues = self.celery_app.control.inspect().active_queues()

        queue_items = []
        for node, val in queues.items():
            queue_items.append(NodeItem(node, val))
        return queue_items

    '''
    Listout all the tasks
    '''
    def get_active_tasks(self) -> list:

        tasks = []
        nodes = self.celery_app.control.inspect().active()

        for vals in nodes.values():
            for task in vals:
                tasks.append(Task(task))
        return tasks

    def get_queue_active_tasks(self, node_name, queue=None) -> list:
        nodes = self.celery_app.control.inspect().active()
        tasks = nodes.get(node_name, [])

        tasks_new = []
        for task in tasks:
            try:
                item = Task(task)
            except Exception as e:
                print("[INFO] not a valid JSON", e)
                continue
            tasks_new.append(item)

        if queue is None:
            return tasks
        
        filtered_tasks = []
        for task in filtered_tasks:
            if task.get('delivery_info', {}).get('routing_key', '') == queue:
                filtered_tasks.append(task)
        
        return filtered_tasks

    def get_pending_queue_len(self, queue: str, conn=None):
        if conn is None:
            conn = self.celery_app.pool.acquire(block=True)
        return conn.default_channel.client.llen(queue)

    def get_pending_tasks_by_queue(self, queue: str, conn=None) -> list:
        if conn is None:
            conn = self.celery_app.pool.acquire(block=True)
        qlen = self.get_pending_queue_len(queue, conn=conn)
        pending_tasks = conn.default_channel.client.lrange(queue, 0, qlen+1)

        tasks = []
        for task in pending_tasks:
            tasks.append(PendingTask(task))

        return tasks
    
    '''
    Returns all the tasks scheduled in on all nodes/workers
    '''
    def get_registered_tasks(self) -> list:
        nodes = self.celery_app.control.inspect().registered()
        tasks = []
        for vals in nodes.values():
            for task in vals:
                try:
                    item = Task(task)
                except Exception as e:
                    print("[INFO] not a valid JSON", e)
                    continue
                tasks.append(item)
        return tasks


class CelmonCLI(Celmon):

    def __init__(self, app_name: str) -> None:
        super().__init__(app_name)

    def loop(self):
        # Refer: https://rich.readthedocs.io/en/latest/live.html
        pass

    def show_active_tasks(self):
        tasks = self.get_active_tasks()

        # Define table header
        table = Table(title="Celery tasks")
        table.add_column("task_id", justify="left", style="cyan", no_wrap=True)
        table.add_column("name", style="red")
        table.add_column("status", style="red")
        table.add_column("time_start", justify="left", style="green")
        table.add_column("queue", justify="left", style="green")

        for task in tasks:
            table.add_row(task.data.get('id', 'NA'),
                task.data.get('name', 'NA'), 
                "Active", 
                task.data.get('time_start', 'NA'),
                task.data.get('delivery_info', {}).get('routing_key'))

        console = Console()
        console.print(table)

    def show_queues(self):
        queues = self.get_queues()
        qlens, names, nodes = [], [], []

        for queue in queues:
            for q in queue.queues:
                names.append(q)
                nodes.append(queue.node)
                qlens.append(self.get_queue_len(queue.node, queue=q))

        table = Table(title="Celery queues")
        table.add_column("queue", justify="left", style="cyan", no_wrap=True)
        table.add_column("node", justify="left", style="cyan")
        table.add_column("number of tasks", style="green")

        for queue, node, qlen in zip(names, nodes, qlens):
            table.add_row(queue, node, qlen)

        console = Console()
        console.print(table)
