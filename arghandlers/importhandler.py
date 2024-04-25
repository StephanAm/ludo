from arghandlers.common import *
from pathlib import Path
from ludocli import *
from urllib.parse import urlparse
import shutil
import subprocess
from ludocommon import setExecPerm, setReadPerm
from os import walk

class ImportHandler(Handler):
    command='import'
    description="""Import game resources from the specfied location."""
    def init(self,subparsers:SubParserAction):
        parser= subparsers.add_parser(self.command,description=self.description)
        addNameArg(parser)

        parser.add_argument(
            '-f', '--force',
            help="""forces resource import.
            By default resource import is skipped when resource have previously been imported.""",
            action='store_true'
        )
        
    def handle(self,args):
        name = changeToGameDirIfProjectDir(args.name)
        failIfNotGameDir()
        force = args.force
        info(f"Importing {name}")
        path = PathManager(name)
        config = loadGameConfig()
        status = loadGameStatus()
        wrapper = self.getWrapper(config,status)
        if force or importRequired(config,status):
            validateConfig(config)
            import_from(config.source, path.packageResource)
            setAccess(path.packageResource)
            wrapper.createMetaFiles()
            self.updateGameStatus(status,config)
        else:
            info("Skipping import")



    def updateGameStatus(self,status:GameStatus,config:GameConfig):
        status.importSource = config.source
        status.wrapTimeStamp = status.importTimeStamp = timeStamp()
        status.wrapConfigHash = status.importConfigHash = config.getHash()
        
        saveGameStatus(status)

        



def import_from_dir(source: Path, dest:Path):
    info(f'importing resources from {source.absolute()}')
    shutil.copytree(
            source,
            dest,
            dirs_exist_ok=True)
    setReadPerm(dest)
    setExecPerm(dest)

def import_from_zip(source: Path, dest:Path):
    info('Import from zip')
    subprocess.run((
        'unzip',
        '-q',
        '-o',
        source.absolute(),
        '-d',
        dest.absolute(),
        ))
    info(f'Extracted to {dest}')

def import_from_local_fs(source:str,dest:Path):
    source = Path(source).expanduser().absolute()
    if not source.exists():
        fail(f"{source} does not exist.")
    if source.is_dir():
        return import_from_dir(source,dest)
    if source.is_file():
        if source.suffix == '.zip':
            return import_from_zip(source, dest)

def setAccess(dest:Path):
    dest = dest.absolute()
    info(f'Setting file access {dest}')
    
    for root,dirs, files in walk(dest):
        root=Path(root).absolute()
        for d in dirs:
            d = root.joinpath(d)
            info(f'Setting perms for {d}')
            setExecPerm(d)
            setReadPerm(d)
        for f in files:
            f = root.joinpath(f)
            setReadPerm(f)

def import_from(source:str,dest:Path):
    dest=dest.absolute()
    dest.mkdir(parents=True,exist_ok=True)
    shutil.rmtree(dest)
    scheme = urlparse(source).scheme
    match scheme:
        case 'file'|'':
            import_from_local_fs(source,dest)
        case _:
            fail(f"Can't import from {scheme} source")
    
    
