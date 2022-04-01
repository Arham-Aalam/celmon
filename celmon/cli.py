from email.policy import default
import os, sys, json
import click

import Celmon, CelmonCLI

@click.command()
@click.option("-A", "--app", prompt="App name", help="Django app name")
@click.option("-qs", "--queues", prompt="Show queues", help="Show queues", default=False)
@click.option("-q", "--queue", prompt="Show queue", help="Provide key name")
def cli(app, show_queues, queue_key):
    celmon = CelmonCLI(app)

# if __name__ == '__main__':
#     args = cli()
    
#     print("[INFO] args: ", args)