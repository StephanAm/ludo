from arghandlers.common import *

create_update_parser = ArgumentParser(add_help=False)
addNameArg(create_update_parser)
create_update_parser.add_argument(
    '-f','--fullname',
    help='The full name of the game',
    default=None)    

create_update_parser.add_argument(
    '-s','--source',
    help='The path containing the application binary and resources',
    default=None
)

create_update_parser.add_argument(
    '-x','--executable', 
    help="""The filename of the main executable. 
    If the executable is not in the source folder, this must be a relative path.
    This argument is optional if the main execuatable is the only BAT or EXE file in the 'source' directory.
    BAT files will take priority if there is one BAT and one EXE file"""
)

create_update_parser.add_argument(
    '-w', '--wrapper',
    help='Specify the wrapper for this game.',
    choices=wrappers.keys(),
    default=None)

create_update_parser.add_argument(
    '-v', '--version',
    help='Specify the verion for this game.',
    default=None)

class CreateHandler(Handler):
    command = "create"
    description = """create a subfolder and config for a game"""
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(
            self.command,
            description=self.description,
            parents=(create_update_parser,))


    def handle(self,args):
        if isProjectDirectory():
            failIfNoGameName(args.name)
            Path(args.name).mkdir(exist_ok=True)
            chdir(args.name)
            name = args.name
        else:
            name = getCwdName()
        
        if loadGameConfig(False):
            fail(f"game directory for {name} is already initialized")

        saveGameConfig(GameConfig(
            name = args.name,
            fullname = args.fullname or name,
            wrapper = args.wrapper,
            runcommand = args.executable,
            source = args.source,
            version = args.version or '0.0.0' 
        ))
        saveGameStatus(GameStatus(
            importTimeStamp=None,
            importSource=None,
            importConfigHash=None,
            wrapTimeStamp=None,
            wrapConfigHash= None,
            buildTimeStamp=None,
            buildConfigHash=None,
            buildNumber=bumpBuild(None)
        ))

class UpdateHandler(Handler):
    command = 'update'
    description = "Update config parameters for the specified game"
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(
            self.command,
            description=self.description,
            parents=(create_update_parser,))
        

    def handle(self,args):
        name = changeToGameDirIfProjectDir(args.name)
        failIfNotGameDir()
        
        info(f'Updating config for {name}')
        
        config = loadGameConfig()
        config = GameConfig(
            name = args.name or config.name,
            fullname = args.fullname or config.fullname,
            wrapper = args.wrapper or config.wrapper,
            runcommand = args.executable or config.runcommand,
            source = args.source or config.source,
            version = args.version or config.version 
        )
        saveGameConfig(config)