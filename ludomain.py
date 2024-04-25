from argparse import ArgumentParser
from ludocommon import * 
from ludocli import *
from ludodataclasses import *
from arghandlers import *
from sys import argv
import subprocess

class ArgHandler:
    def __init__(self,) -> None:
        self.parser = ArgumentParser(
            'ludo',
            description='Wraps dos or windows applications to be launched with Dosbox or Wine')
        self.subparsers = self.parser.add_subparsers(title='command',dest='command', required=True)
        self.handlers = {}

    def addHandler(self,handlerCls:Handler):
        handler = handlerCls()
        handler.init(self.subparsers)
        self.handlers[handler.command] = handler.handle

    def parseArgs(self, args=None):
        args = self.parser.parse_args(args=args)
        self.handlers[args.command](args)

def setupHandler():
    argHandler = ArgHandler()
    argHandler.addHandler(ImportHandler)
    argHandler.addHandler(ListHandler)
    argHandler.addHandler(InitHandler)
    argHandler.addHandler(CreateHandler)
    argHandler.addHandler(UpdateHandler)
    argHandler.addHandler(EditHandler)
    argHandler.addHandler(StatusHandler)
    argHandler.addHandler(BuildHandler)
    argHandler.addHandler(IconHandler)
    argHandler.addHandler(WrapHandler)
    return argHandler

def interactiveMode(handler):
    while True:
        x = input('ludo: ').strip()
        if x in ('quit','exit'):
            break;
        try:
            handler.parseArgs(x.split())
        except FailError: 
            continue

def main(args = None):
    handler = setupHandler()
    if len(argv) == 2 and argv[1] == 'cli':
        interactiveMode(handler)
    else:
        handler.parseArgs(args=args)