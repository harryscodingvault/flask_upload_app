from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('A username is require'), Length(max=100, message='Your username can not be over 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('A password is required')])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('A username is require'), Length(max=100, message='Your username can not be over 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('A password is required')])
    remember = BooleanField('Remember me')

class RegisterAlbumForm(FlaskForm):
    album_name = StringField('Name', validators=[InputRequired('A name is require'), Length(max=100, message='Your album name can not be over 100 characters.')])

class ImageUploadForm(FlaskForm):
    image = FileField(validators=[FileAllowed(IMAGES, 'Only images are accepted.')])