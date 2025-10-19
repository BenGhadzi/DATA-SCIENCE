from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#Hashing out the password and protecting passwords of users
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail #After import, set constants (mail server, mail port, USE_tls, username and password) for the server
from flasktutor.config import  Config



# the /// in the database name suggest that the db file is in the same project dir
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
#This decorate the message returned by searching account on the web directly
login_manager.login_message_category = 'info'
#To redirect directly to the page we were trying to access before we were asked to login first
#route import request and add on to the login route.

mail = Mail() #call it in the routes



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flasktutor.users.routes import users
    from flasktutor.posts.routes import posts
    from flasktutor.main.routes import main
    from flasktutor.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
