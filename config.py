import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT','465'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # STREAM_API_KEY = os.environ.get('STREAM_API_KEY')
    # STREAM_SECRET = os.environ.get('STREAM_SECRET')
    #S3_BUCKET = os.environ.get('S3_BUCKET')
    #S3_KEY = os.environ.get('S3_KEY')
    #S3_SECRET = os.environ.get('S3_SECRET_ACCESS_KEY')
    WEB_ADMIN = os.environ.get('WEB_ADMIN')
    ADMINS = ['']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 10
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    SITE_WIDTH = 600
