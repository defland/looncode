#coding:utf-8


class DevelopmentConfig():
    DEBUG = True
    SECRET_KEY='123456'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./application/db/learoom.db'
    REDIS_DATABASE_URL = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWD = ''
    REDIS_CACHE_TIME = 86400
    GIT_VERSION_DISPLAY = False
    pass


class TestingConfig():
    DEBUG = True
    TESTING = True
    SECRET_KEY='123456'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./application/db/learoom.db'
    REDIS_DATABASE_URL = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWD = ''
    GIT_VERSION_DISPLAY = False
    pass

class ProductionConfig():
    DEBUG = False
    SECRET_KEY='123456'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./application/db/learoom.db'
    REDIS_DATABASE_URL = 'localhost'
    REDIS_PORT = 6379
    REDIS_PASSWD = ''
    GIT_VERSION_DISPLAY = False
    pass


config = {
    
    "dev":DevelopmentConfig,
    "test":TestingConfig,
    "product":ProductionConfig,
    "default":DevelopmentConfig
}

