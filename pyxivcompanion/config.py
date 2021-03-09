from .utility import classproperty

class Config:
    APP_VERSION = "1.11.2"
    GLOBAL_COMPANION_BASE_URL = 'https://companion.finalfantasyxiv.com/'
    SIGHT_PATH = 'sight-v060/sight/'

    @classproperty
    def GLOBAL_COMPANION_BASE(cls):
        return cls.GLOBAL_COMPANION_BASE_URL + cls.SIGHT_PATH
        
    SECURE_SQUARE_ENIX_URL_BASE = 'https://secure.square-enix.com/'
