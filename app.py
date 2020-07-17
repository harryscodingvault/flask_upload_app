from flask import Flask
app = Flask(__name__)


@app.route('/')
def homepage():
    pass


@app.route('/update_user', methods=['POST'])
def update_user():
    pass

@app.route('/login/<string:name>')
def login(name):
    pass

@app.route('/logout')
def logout(name):
    pass



@app.route('/album_list/')
def create_album():
    pass


@app.route('/album_list/<string:album_name>')
def check_album(album_name):
    pass


app.run(port=5000)