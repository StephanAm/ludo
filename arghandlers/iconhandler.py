from arghandlers.common import *
from shutil import copyfile

class IconHandler(Handler):
    command = "icon"
    description="""Initialize a new Ludo project in the current location"""
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)
        addNameArg(parser)
        parser.add_argument(
            'iconpath',
            help='path to the icon that must be imported',
            action='store'
        )

    def handle(self,args):
        name = changeToGameDirIfProjectDir(args.name)
        paths = PathManager(name)
        info(f'Importing icon for {name}.')
        source = Path(args.iconpath).expanduser().absolute()
        if not source.exists():
            fail(f"{source} does not exist")
        paths.packageMeta.mkdir(parents=True,exist_ok=True)
        copyfile(source,paths.packageIcon)
        info("Icon imported")
        

        
