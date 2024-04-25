from arghandlers.common import *
class InitHandler(Handler):
    command = "init"
    description="""Initialize a new Ludo project in the current location"""
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)

    def handle(self,_):
        if isProjectDirectory():
            fail("This is path has already been initialized as a Ludo project")
        initProjectDirectory()