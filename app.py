from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, PasswordField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_photos.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(50))

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('A username is requirede'), Length(max=100, message='Your username can not be over 100 characters.')])
    password = PasswordField('Password', validators=[InputRequired('A password is required')])

class ImageUploadForm(FlaskForm):
    image = FileField()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    #if form.validate_on_submit():

    return render_template('register.html', form = form)

@app.route('/login')
def login():
    return render_template('login.html')

#@app.route('/<album>/<photo>')
#def show_photos():
    #return render_template('index.html')

#@app.route('/<album>')
#def show_album():
    #return render_template('index.html')

if __name__ == '__main__':
    manager.run()
    