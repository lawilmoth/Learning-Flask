import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard_to_guess_string"
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT',  '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME= os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SUBJECT_PREFIX= "[My App]"
    MAIL_SENDER = 'Flask Admin'
    ADMIN = os.environ.get('ADMIN') or 'lwilmoth@eriesd.org'
    SQLALCHEMY_TRACK_MODIFICATION = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or\
        'sqlite:///'+os.path.join(basedir,'data.sqlite')
    
    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or\
        'sqlite:///'+os.path.join(basedir,'test_data.sqlite') #add this
    
    

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or\
        'sqlite:///'+os.path.join(basedir,'data.sqlite')
    
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
    
    