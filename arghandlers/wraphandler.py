from arghandlers.common import *
class WrapHandler(Handler):
    command='wrap'
    description="""Regenerate the relevant meta files. Same as import, but skips the import part completely"""
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)
        addNameArg(parser)

        parser.add_argument(
            '-f', '--force',
            help="""forces meta file generation.""",
            action='store_true'
        )

        
    def handle(self,args):
        name = changeToGameDirIfProjectDir(args.name)
        failIfNotGameDir()
        force = args.force
        info(f"Importing {name}")
        config = loadGameConfig()
        status = loadGameStatus()
        wrapper = self.getWrapper(config,status)
        if force or wrapRequired(config,status):
            validateConfig(config)
            wrapper.createMetaFiles()
            self.updateGameStatus(status,config)
        

    def updateGameStatus(self,status:GameStatus,config:GameConfig):
        status.wrapTimeStamp = timeStamp()
        status.wrapConfigHash = config.getHash()
        saveGameStatus(status)

