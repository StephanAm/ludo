from dataclasses import dataclass,field,asdict,astuple
import datetime
from pathlib import Path
from ludocli import *
import json
import ludopaths
import shutil
import hashlib

from_iso_time = datetime.datetime.fromisoformat

class jsonDataCls:
    @classmethod
    def load(cls,src:Path):
        with open(src) as f:
            d = json.load(f)
        return cls(**d)
        
    def save(self,dst:Path):
        with open(dst, 'w') as f:
            json.dump(self.asdict(),f,indent='\t')

    def asdict(self):
        return asdict(self)

    def getHash(self):
        return hashlib.md5(json.dumps(self.asdict()).encode('utf-8')).hexdigest()
        

@dataclass(kw_only=True)
class GameStatus(jsonDataCls):

    importTimeStamp:str
    importSource:str
    importConfigHash:str
    
    wrapTimeStamp:str
    wrapConfigHash:str
    
    buildTimeStamp:str
    buildConfigHash:str
    buildNumber:int
    

@dataclass(kw_only=True)
class GameConfig(jsonDataCls):
    name:str
    fullname:str
    wrapper:str
    runcommand:str
    source:str
    version:str

    
def configExists(name:str = None):
    p = Path(name) if name else Path()
    p = p.joinpath(ludopaths.PathManager.config_file)
    return p.exists()

def loadGameConfig(fail_if_no_config:bool=True) -> GameConfig:
    file = ludopaths.PathManager.getConfigFilePath()
    return loadGameConfigFromPath(file,fail_if_no_config)

def loadGameConfigFromPath(file: Path, fail_if_no_config:bool=True) -> GameConfig:
    if not file.exists():
        if fail_if_no_config:fail(f'loadGameConfig: {file.absolute()} does not exist')
        else: return None
    return GameConfig.load(file)
    

def saveGameConfig(config:GameConfig):
    file = ludopaths.PathManager.getConfigFilePath()
    bck_path = ludopaths.PathManager.getBackupConfigFilePath()
    saveGameConfigToPath(config, file, bck_path)


def saveGameConfigToPath(config:GameConfig, file:Path, backUpPath:Path = None):
    if config == loadGameConfigFromPath(file,fail_if_no_config=False):
        return
    
    if backUpPath and file.exists():
        shutil.copyfile(file,backUpPath)
    config.save(file)

def hasValidImport(config:GameConfig = None, import_status:GameStatus = None):
    config = config or loadGameConfig()
    import_status = import_status or loadGameStatus()
    return config.source == import_status.importSource

def loadGameStatus()->GameStatus:
    file = Path(ludopaths.PathManager.import_file)
    
    if not file.exists():
        return GameStatus(importSource=None,importTimeStamp=None)

    return GameStatus.load(file)

def saveGameStatus(status:GameStatus):
    file = Path(ludopaths.PathManager.import_file)
    status.save(file)
    info('Status Updated')

def bumpBuild(build:str)->str:
    if not build:
        count = 1
    else:
        count = int(build.rsplit('.',1)[-1]) + 1

    return f'{datetime.datetime.now().strftime("%y%m%d")}.{count}'

def timeStamp() -> str:
    return str(datetime.datetime.now())


def importRequired(config:GameConfig, status: GameStatus):
    if not status.importTimeStamp:
        info('Last import time not set, wrap required')
        return True
    
    if config.source != status.importSource:
        info('Source has changed import required')
        return True
    
    info ('Import is up to date')
    return False


def wrapRequired(config:GameConfig, status: GameStatus):
    if not status.wrapTimeStamp:
        info('Last wrap time not set, wrap required')
        return True

    if not status.importTimeStamp:
        warn("No resource import, can't build")
        return False
    
    if config.getHash() != status.wrapConfigHash:
        info('Config has changed, wrap required')
        return True
    
    info ('Wrap is up to date')
    return False

def buildRequired(config:GameConfig, status:GameStatus):
    if not status.buildTimeStamp:
        info('Last build time not set, build required')
        return True
    if not status.wrapTimeStamp:
        warn("No wrap, can't build")
        return False
    
    if config.getHash() != status.buildConfigHash:
        info('Config has changed, build required')
        return True
    
    if from_iso_time(status.wrapTimeStamp) > from_iso_time(status.buildTimeStamp):
        info('Resources have been imported since last build, build required')
        return True
    
    info ('No resource or config changes since last build')
    return False