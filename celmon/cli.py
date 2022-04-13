import os, sys, json
import argparse

from .core import Celmon, CelmonCLI


def cli(app, show_queues, queue_key):
    print("====> ", app, show_queues, queue_key)
    celmon = CelmonCLI(app)
    celmon.show_queues()


def show_pending_tasks(app, queue):
    cli = CelmonCLI(app)
    cli.show_pending_tasks(queue=queue)


def set_options():
    parser = argparse.ArgumentParser(prog="celmon",
        usage="python %(prog)s [options]",
        description="A command-line monitoring tool for celery.")
    parser.add_argument("-A", "--app", help="App name.")
    parser.add_argument("-qs", "--queues", help="Show queues.", action="store_true")
    parser.add_argument("-pt", "--pending_tasks", help="Show all pending tasks for a queue.", action="store_true")
    parser.add_argument("-at", "--active_tasks", help="Show all active tasks for queue or all queues.", action="store_true")
    parser.add_argument("-q", "--queue", help="Queue name")
    parser.add_argument("-pdt", "--periodic_tasks", help="Show scheduled tasks.")
    parser.add_argument("-l", "--live", help="flag for live update", action="store_true")

    args = parser.parse_args()
    return args

def validate_args(args):
    if not args.app:
        raise ValueError("Please provide argument --app or -A")

def start_monitoring(args):
    cli = CelmonCLI(args.app)

    if args.qs:
        cli.show_queues()

    if args.active_tasks:
        cli.show_active_tasks(queue=args.queue)

    if args.pending_tasks:
        cli.show_pending_tasks(queue=args.queue)

    if args.periodic_tasks:
        cli.show_pending_tasks(queue=args.queue)

    if args.live:
        # TODO run loop with status
        raise NotImplemented()

def run_cli():
    args = set_options()
    validate_args(args)
    start_monitoring()

# if __name__ == '__main__':
#     args = cli()
    
#     print("[INFO] args: ", args)