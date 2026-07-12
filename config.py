import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:altair123m@localhost/sakuranet"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False