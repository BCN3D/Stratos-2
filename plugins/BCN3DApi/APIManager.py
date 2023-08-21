from .PrintersManager import PrintersManager
from .AuthApiService import AuthApiService
from PyQt6.QtCore import QObject, pyqtSlot
from UM.PluginRegistry import PluginRegistry


class APIManager(QObject):
    _authentication_service = None
    _printers_manager = None

    def __init__(self):
        super().__init__()
        if self.__instance is not None:
            raise ValueError("Duplicate singleton creation")
        self._authentication_service = None
        self._printers_manager = None
        self._printers_manager = PrintersManager.getInstance()

    @pyqtSlot(result=AuthApiService)
    def getAuthenticationService(self):
        if self._authentication_service is None:
            self._authentication_service = AuthApiService.getInstance()
            self._authentication_service.startApi()
        return self._authentication_service

    @pyqtSlot(result=PrintersManager)
    def getPrintersManager(self):
        if self._printers_manager is None:
            self._printers_manager = PrintersManager.getInstance()
        return self._printers_manager

    @classmethod
    def getInstance(cls) -> "APIManager":
        if not cls.__instance:
            cls.__instance = APIManager()
        return cls.__instance
    
    __instance = None



