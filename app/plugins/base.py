from abc import ABC, abstractmethod
from telegram.ext import Application

class BasePlugin(ABC):
    @abstractmethod
    def register_handlers(self, app: Application):
        pass

    @abstractmethod
    def get_metadata(self):
        return {
            "name": "Unnamed Plugin",
            "version": "0.1"
        }