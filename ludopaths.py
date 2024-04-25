from pathlib import Path
from os import listdir
from ludocommon import *

class PathManager:
    config_file = 'ludo.cfg'
    config_backup_file = '.ludo.cfg.bck'
    project_file = '.ludoproject'
    import_file = '.status'
    icon_file = 'icon.png'

    def __init__(self, name = None) -> None:
        if name:
            self.setPaths(name)

    def setPaths(self, name):
        binPath = f'./usr/local/bin/'
        resourcePath = f'./usr/local/{name}/resource'
        metaPath = f'./usr/local/{name}/meta'
        applicationsPath = './usr/share/applications/'
        desktopFileName = f'ludo.application.{name}.desktop'
        
        self.gameConfigFile = self.getConfigFilePath()
        self.importFile = self.getImportFilePath()

        # package paths (paths relative to project root)
        packageRoot = Path().joinpath(f'./package')
        self.debRoot = packageRoot.joinpath('DEBIAN')
        self.debControlFile = self.debRoot.joinpath('control')
        
        self.packageResource = packageRoot.joinpath(resourcePath)
        self.packageMeta = packageRoot.joinpath(metaPath)
        self.packageBin = packageRoot.joinpath(binPath)
        self.packageApplications = packageRoot.joinpath(applicationsPath)
        
        self.packageIcon = self.packageMeta.joinpath(self.icon_file)
        self.packageDesktopFile = self.packageApplications.joinpath(desktopFileName)
        self.packageLauncher = self.packageBin.joinpath(name)

        # absolute paths (used for generating final deb package)
        absRoot = Path('/')        
        self.absResource = absRoot.joinpath(resourcePath)
        self.absMeta = absRoot.joinpath(metaPath)
        self.absBin = absRoot.joinpath(binPath)
        self.absApplications = absRoot.joinpath(applicationsPath)
        
        self.absIcon = self.absMeta.joinpath(self.icon_file)
        self.absDesktopFile = self.absApplications.joinpath(desktopFileName)
        self.absLauncher = self.absBin.joinpath(name)
    

    @classmethod
    def getConfigFilePath(cls) -> Path:
        return Path().joinpath(cls.config_file)

    @classmethod
    def getBackupConfigFilePath(cls) -> Path:
        return Path().joinpath(cls.config_backup_file)
    

    
    @classmethod
    def getImportFilePath(cls) -> Path:
        return Path().joinpath(cls.import_file)


class TEMPLATE_PATHS:
    ROOT = Path('/usr/local/ludo/templates')
    DOSBOX_CONF = ROOT.joinpath('dosbox.conf.template')
    DOSBOX_DEB_CONTROL = ROOT.joinpath('dosbox.control.template')
    DOSBOX_LAUNCHER = ROOT.joinpath('dosbox.launcher.template')
    WINE_DEB_CONTROL = ROOT.joinpath('wine.control.template')
    WINE_LAUNCHER = ROOT.joinpath('wine.launcher.template')
    DESKTOP_FILE = ROOT.joinpath('desktop.template')