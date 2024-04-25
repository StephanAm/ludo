import subprocess
from os import listdir
from pathlib import Path
from argparse import ArgumentParser,_SubParsersAction
from ludocommon import * 
from ludocli import *
from ludowrapper import Wrapper,wrappers
from ludopaths import PathManager

SubParserAction = _SubParsersAction


def addNameArg(parser: ArgumentParser):
        parser.add_argument(
            'name',
            help="""name of the application.
            Prefer lower case with no special characters.""",
            nargs='?',
            default=None
        )
class Handler:
    @property
    def command(self): raise NotImplementedError()
    
    @property
    def description(self): raise NotImplemented

    def init(self,subparsers:SubParserAction): raise NotImplemented
    
    def handle(self,args): raise NotImplemented

    
    def getWrapper(self, config: GameConfig, status:GameStatus)->Wrapper:
        return wrappers[config.wrapper](config,status)










