import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/databaseFap'
    SQLALCHEMY_TRACK_MODIFICATION = False