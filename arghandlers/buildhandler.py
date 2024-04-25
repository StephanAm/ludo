from arghandlers.common import *

class BuildHandler(Handler):
    command = 'build'
    description = 'package the game'
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)
        addNameArg(parser)
        parser.add_argument(
            '-f','--force',
            help = 'Force the build',
            action = 'store_true'
        )

    def handle(self,args):
        name = changeToGameDirIfProjectDir(args.name)
        failIfNotGameDir()
        force:bool = args.force
        gameStatus = loadGameStatus()
        gameConfig = loadGameConfig()
        if force or buildRequired(gameConfig, gameStatus):
            self.doBuild(name)
            self.updateGameStatus(gameStatus, gameConfig)

        else:
            info('Skipping build')

    def doBuild(self,name):
        try:
            subprocess.run(
                ("dpkg-deb", "--root-owner-group", "-b", f"./package", f"{name}.deb")
                ,check=True
                )
        except subprocess.CalledProcessError:
            fail(f"Failed to package {name}")
        info('Package built successfully.')
    
    def updateGameStatus(self, status: GameStatus, config: GameConfig):
        status.buildNumber = bumpBuild(status.buildNumber)
        status.buildTimeStamp = timeStamp()
        status.buildConfigHash = config.getHash()
        saveGameStatus(status)