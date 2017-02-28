#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager
from flask_script import Flask
from flask_script import Command
from nagioscli import manager as nagman
from awsiam import manager as awsman


from argparse import ArgumentParser


app = Flask(__name__)
# configure your app

manager = Manager(app)


class Hello(Command):
    "prints hello world"

    def run(self):
        print("hello world almighty")

    def __str__(self):
        return "yay"


@manager.command
def hello():
    "Just say hello"
    print("hello")

manager.add_command("nagios", nagman)
manager.add_command("aws", awsman)

if __name__ == "__main__":
    manager.run()