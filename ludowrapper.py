# import os
from os import listdir
from pathlib import Path
from ludocommon import *
from ludocli import fail,info,warn
from ludocommon import GameConfig
from ludopaths import PathManager,TEMPLATE_PATHS

class Wrapper:
    def createLauncher(self): raise NotImplementedError("override this method")
    def createDebControl(self): raise NotImplementedError("override this method")
    
    def __init__(self,config:GameConfig,status:GameStatus) -> None:
        name = config.name
        self.name = name
        if not name:
            raise ValueError('Expected "name" in Wrapper initiliazer')
        self.config = config
        self.status = status
        exec = config.runcommand
        source = config.source
        if not source:
            fail("No source has been configured")
        
        self.paths = PathManager()
        self.paths.setPaths(name)
        
    # def importResources(self):
        
    #     self.paths.packageResource.mkdir(parents=True,exist_ok=True)
    #     import_from(
    #         self.config.source,
    #         self.paths.packageResource
    #     )
        
    def createMetaFiles(self):
        if not self.paths.importFile.exists():
            fail("Can't generate meta files, resources have not been imported")
        info("Create meta file directory structure")
        self.paths.packageResource.mkdir(parents=True, exist_ok=True)
        self.paths.packageMeta.mkdir(parents=True,exist_ok=True)
        self.paths.packageBin.mkdir(parents=True, exist_ok=True)
        self.paths.packageApplications.mkdir(parents=True, exist_ok=True)
        self.createDesktopFile()
        self.createDebControl()
        self.createLauncher()
  
    def createDesktopFile(self):
        processFileTemplate(
            TEMPLATE_PATHS.DESKTOP_FILE,
            self.paths.packageDesktopFile,
            {
                'version': self.config.version,
                'fullname': self.config.fullname,
                'comment':'',
                'name': self.config.name,
                'icon': self.paths.absIcon,
                'exec': self.paths.absLauncher,
                'path': self.paths.absResource,
            }
        )



  
class WineWrapper(Wrapper):
    wrapperType='wine'
    
    def __init__(self, config: GameConfig, status: GameStatus) -> None:
        super().__init__(config,status)
        self.finalExecPath = self.paths.absResource.joinpath(config.runcommand)


    def createDebControl(self):
        info('Create .deb package meta files')
        self.paths.debRoot.mkdir(parents=True,exist_ok=True)
        subs={
            'version':self.config.version,
            'packagename':self.name,
            'fullname':self.config.fullname
        }
        processFileTemplate(
            TEMPLATE_PATHS.WINE_DEB_CONTROL,
            self.paths.debControlFile,
            subs
        )
    
    def createLauncher(self):
        info('Create launcher')
        processFileTemplate(
            TEMPLATE_PATHS.WINE_LAUNCHER,
            self.paths.packageLauncher,
            {
                'executable':self.finalExecPath
            }
        )
        info('making launcher executable')
        setExecPerm(self.paths.packageLauncher)

class DosBoxWrapper(Wrapper):
    wrapperType='dosbox'
    def __init__(self,config:GameConfig,status:GameStatus) -> None:
        super().__init__(config,status)
        self.packageDosboxConfigFile = self.paths.packageMeta.joinpath(f'./{self.name}.conf')
        self.absDosboxConfigFile = self.paths.absMeta.joinpath(f'./{self.name}.conf')

    def createMetaFiles(self):
        super().createMetaFiles()
        self.createDosBoxConf()

    def createDosBoxConf(self):
        info('Create DosBox config file')
        subs = {
            'resourcepath':self.paths.absResource,
            'execcommand': self.config.runcommand
        }

        processFileTemplate(
            TEMPLATE_PATHS.DOSBOX_CONF,
            self.packageDosboxConfigFile,
            subs=subs
        )
      
    def createLauncher(self):
        info('Create launcher')
        subs = {
            'dosboxconfig':self.absDosboxConfigFile.absolute()
        }
        processFileTemplate(
            TEMPLATE_PATHS.DOSBOX_LAUNCHER,
            self.paths.packageLauncher,
            subs
        )
        setExecPerm(self.paths.packageLauncher)

    def createDebControl(self):
        info('Create .deb package meta files')
        self.paths.debRoot.mkdir(parents=True,exist_ok=True)
        subs={
            'version':f'{self.config.version}-{self.status.buildNumber}',
            'packagename':self.name,
            'fullname':self.config.fullname
        }
        processFileTemplate(
            TEMPLATE_PATHS.DOSBOX_DEB_CONTROL,
            self.paths.debControlFile,
            subs
        )

wrappers = {
        'wine':WineWrapper,
        'dosbox': DosBoxWrapper
    }