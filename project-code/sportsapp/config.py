
class Config:
    #some generated list of 16 hex values (used for passwords and validation)
    SECRET_KEY='0819780287c1fe01cfb39284c1c55b7d'
    #creating database on file system for now using sqlite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'