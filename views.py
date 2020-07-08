import os
from app import app, photos, db
from models import User, Album, Photo
from forms import RegisterForm, LoginForm, RegisterAlbumForm, ImageUploadForm
from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, logout_user
from werkzeug import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    photos = Photo.query.all()
    albums = Album.query.all()
    return render_template('index.html', photos = photos, albums=albums)

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

@app.route('/photo_upload/<album_id>')
def uploaded_file(album_id):
    return render_template('upload.html', photos=photos, album_id = album_id)

@app.route('/delete_photo/<album_id>/<photo_id>')
def delete_photo(photo_id, album_id):
    item_to_delete = Photo.query.get_or_404(photo_id)
    
    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect(f'/photo_upload/{album_id}')
    except:
        return 'There was a problem deleting that task'

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

@app.route('/delete_album/<album_id>')
def delete_album(album_id):
    album_to_delete = Album.query.get_or_404(album_id)
    try:
        db.session.delete(album_to_delete)
        db.session.commit()
        return redirect('/album_menu')
    except:
        return 'There was a problem deleting that task'

