
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_photos.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

login_manager = LoginManager(app)
login_manager.login_view = 'login'

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)



from views import *

manager = Manager(app)
manager.add_command('db', MigrateCommand)



if __name__ == '__main__':
    manager.run()
    