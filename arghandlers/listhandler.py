from arghandlers.common import *
class ListHandler(Handler):    
    command="list"
    description="List all imported games"
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)

    def handle(self,args):
        failIfNotProjectDir()
        projectRoot = Path('.')
        for dir in listdir(projectRoot):
            if configExists(dir):
                print(dir)