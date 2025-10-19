import os


class Config:
    # SeCRET_KEY value is a confidential item and needs to be treated like the email and password
    SECRET_KEY = 'b5db0870dd30687d0f8b7c68b980318da53d6563ed78b9a8b3df2b35859ac91f2179d86c4eec6b57a7965037836723c7309f2cb912d0ad73e82ceed540df11f6'
    #Below is the cofig code for the sqlite set in the App folder
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'site.db')
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    # EMAIL_USER AND EMAIL_PASS have to be set up under environment variables to secure username and password.
    #After config, we need to initialize mail as below
