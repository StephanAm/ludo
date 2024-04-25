from pathlib import Path
from string import Template
from ludocli import fail,warn,error
from ludodataclasses import *
from ludopaths import PathManager
from os import chdir

from stat import S_IXUSR,S_IXGRP,S_IXOTH,S_IRUSR,S_IRGRP,S_IROTH

AX = S_IXGRP|S_IXOTH|S_IXUSR
AR = S_IRGRP|S_IROTH|S_IRUSR

def setReadPerm(target: Path):
    target.chmod(target.stat().st_mode | AR)

def setExecPerm(target: Path):
    target.chmod(target.stat().st_mode | AX)

def coalesce(*args):
    for a in args:
        if a:
            return a
    return None

def processFileTemplate(template:Path|str, outputFile:Path|str, subs:dict):
    template=Path(template)
    outputFile=Path(outputFile)
    with open(template) as t, open(outputFile,'w') as o:
        for l in t:
            o.write(Template(l).substitute(subs))
        
def validateConfig(config:GameConfig):
    hasFailed = fail
    if not config.wrapper:
        error('No wrapper has been specified')
        hasFailed = True
    if not config.source:
        error('No source has been specified')
        hasFailed = True
    if not config.runcommand:
        warn('No executable has been specified')
    return hasFailed


def isProjectDirectory():
    r =  Path(PathManager.project_file).exists()
    return r

def isGameDirectory():
    r = Path(PathManager.config_file).exists()
    return r

def initProjectDirectory():
    Path(PathManager.project_file).touch()
    
def failIfNotProjectDir():
    if not isProjectDirectory():
        fail("This is not a Ludo project folder.")

def failIfNotGameDir():
    if not isGameDirectory():
        fail("This is not a Ludo project folder.")

def failIfNoGameName(name):
    if not name:
        fail("Game name must be specified when running from project root")
def getCwdName():
    return Path().absolute().name

def changeToGameDirIfProjectDir(name):
    """If currently running from a project directory, will change into the specified game directory.
    returns the name of the game
    """
    if isProjectDirectory():
        failIfNoGameName(name)
        chdir(Path(name))
    elif isGameDirectory():
        name = getCwdName()
    return name

