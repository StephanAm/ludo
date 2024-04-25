from arghandlers.common import *

class EditHandler(Handler):
    command = "edit"
    description="""Interactively edit the config for the specified game"""
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)
        addNameArg(parser)

    def handle(self,args):
        name = changeToGameDirIfProjectDir(args.name)
        info(f'Editing config for {name}.')
        failIfNotGameDir()
        info(f'Hit enter to keep existing value')
        config = loadGameConfig()
        config.name=askForValue('name',config.name)
        config.fullname=askForValue('fullname', config.fullname)
        config.runcommand=askForValue('runcommand',config.runcommand)
        config.source=askForValue('source',config.source)
        config.version=askForValue('version',config.version)
        config.wrapper=askForValue('wrapper',config.wrapper,choices=wrappers.keys())
        saveGameConfig(config)