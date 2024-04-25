from arghandlers.common import *
class StatusHandler(Handler):
    command = 'status'
    description = "Show detail for the specified game"
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)
        addNameArg(parser)

    def handle(self,args):
        name = changeToGameDirIfProjectDir(args.name)
        paths = PathManager(name)
        failIfNotGameDir()
        config = loadGameConfig(name)
        status = loadGameStatus()
        
        info('CONFIG')
        self.printTable(config.asdict())
        info(f'Hash: {config.getHash()}')
        print()
        info('STATUS')
        self.printTable(status.asdict()) 
        print()

        if not paths.packageIcon.exists():
            warn("No icon has been imported")

        if not status.importTimeStamp:
            warn("Resources have not been imported. Run ludo import [game] to import")

        if status.importSource != config.source:
            warn("The 'source' has changed since the last update")

        if not config.source:
            warn("'source' value must be set before trying to import")
        if not config.runcommand:
            warn("'runcommand' has not been set. Ludo will try a best guess on import")

        if importRequired(config,status):warn('Import required')
        if wrapRequired(config,status): warn('Wrap required')
        if buildRequired(config,status): warn('Build required')

  
        
    def printTable(self,data:dict):
        items = data.items()
        width = 2+max(len(k) for k,_ in items)
        for k,v in items:
            color = ui.green if v else ui.yellow
            info(f"{k.ljust(width)} : {v}",color)