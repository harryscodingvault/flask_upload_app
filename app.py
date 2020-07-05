import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug import secure_filename
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

manager = Manager(app)
manager.add_command('db', MigrateCommand)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))    

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    image = db.Column(db.String(100))

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        #Database
        new_user = User(username = form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if not user:
            return render_template('login.html', form=form, message='Login failed')

        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            return redirect(url_for('profile'))

        return render_template('login.html', form=form, message='Login failed')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')

@app.route('/photo_upload/<album_id>', methods=['GET','POST'])
def photo_upload(album_id):
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
            filenames.append(filename)
            file_url = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename)
            file_url = '..\\' + file_url
            #Database
            new_photo  = Photo(image=file_url, album_id= album_id)
            db.session.add(new_photo)
            db.session.commit()
    
    photos = Photo.query.filter_by(album_id=album_id).all()
    return render_template('upload.html', photos=photos, album_id = album_id)

@app.route('/photo_upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)
    

@app.route('/album_menu', methods=['GET', 'POST'])
def album_menu():
    form = RegisterAlbumForm()
    if form.validate_on_submit():
        new_album = Album(name = form.album_name.data)
        db.session.add(new_album)
        db.session.commit()
        return redirect(url_for('album_menu'))
    
    albums = Album.query.all()
    photos = Photo.query.all()

    return render_template('list_album.html', form = form, albums=albums, photos=photos)

@app.route('/my_albums', methods=['GET', 'POST'])
def my_albums():
    albums = Album.query.all()
    photos = Photo.query.all()

    return render_template('my_albums.html', photos = photos, albums=albums)

if __name__ == '__main__':
    manager.run()
    