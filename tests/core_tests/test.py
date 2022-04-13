import unittest
from celmon.core import CelmonCLI

class CoreTest(unittest.TestCase):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.cli = CelmonCLI('django_app')

    def test_queues(self):
        self.cli.show_queues()

    def test_active_tasks(self):
        self.cli.show_active_tasks()

    def test_pending_tasks(self):
        self.cli.show_pending_tasks()

    def test_pending_tasks_by_queue(self):
        self.cli.show_pending_tasks(queue='important')

    # def test_periodic_tasks(self):
    #     self.cli.show_periodic_tasks()

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()