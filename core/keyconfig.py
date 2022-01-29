import os

class Database:
    NAME = os.getenv('POSTGRES_DB')
    USER = os.getenv('POSTGRES_USER')
    PASSWORD = os.getenv('POSTGRES_PASSWORD')
    HOST = os.getenv('DATABASE_HOST')
    PORT = os.getenv('DATABASE_PORT')

class Sendgrid:
    KEY = os.getenv('SENDGRID_API_KEY') 

class Django:
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

class AllAuth:
    CLIENT_ID= os.getenv('CLIENT_ID') 
    SECRET = os.getenv('SECRET')

    

