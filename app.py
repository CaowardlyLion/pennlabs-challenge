import os
import bcrypt
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE}"
app.config['UPLOAD_FOLDER'] = "files/"
app.config['MAX_CONTENT_PATH'] = 8000000


db = SQLAlchemy(app)

from models import *


login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

# Simple get route that was used for testing
# @app.route('/get/', methods = ['GET'])
# def get():
#     args = request.args
#     username = args.get("username")
#     return User.query.filter_by(username = username).first().name

@app.route('/api/clubs', methods = ['GET'])
def clubs():
    query = Club.query.all()
    parsed = [i.to_dict() for i in query]
    return jsonify(parsed)

# Profile route: looks for user with a certain username; if none exists, return empty dictionary
@app.route('/api/profile', methods = ['GET'])
def profile():
    args = request.args
    username = args.get("username")

    query = User.query.filter_by(username = username).one_or_none()
    if query is not None:
        # to_dict returns 
        return jsonify(query.to_dict())
    else:
        return jsonify({})

@app.route('/api/search', methods = ['GET'])
def search():
    args = request.args
    q = args.get("query")
    query = Club.query.filter(Club.name.contains(q)).all()
    names = [i.name for i in query]
    return jsonify(names)

@app.route('/api/add', methods = ['POST'])
def add():
    # code = db.Column(db.String(20), unique=True, nullable=False, primary_key = True)
    # name = db.Column(db.String(60), nullable=False)
    # description = db.Column(db.Text(), nullable=False)
    # tags = db.Column(db.Text())

    code = request.form.get("code")
    name = request.form.get("name")
    description = request.form.get("description")   
    query = Club.query.filter_by(code = code).one_or_none()
    if query is not None:
        return jsonify({"Error:" : "Club already exists with that code."}), 400
    club = Club(code = code,
        name = name,
        description = description,
        tags = json.dumps(request.form.getlist("tags")))
    db.session.add(club)
    db.session.commit()
    return {}

from flask_login import login_required, current_user

@app.route('/api/favorite', methods = ['POST'])
# @login_required
def favorite():
    id = request.form.get("id")
    clubid = request.form.get("clubid")
    query = User.query.filter_by(id = id).one_or_none()
    clubquery = Club.query.filter_by(code = clubid).one_or_none()

    loginip = request.remote_addr
    if query == current_user:
        if query is not None and clubquery is not None:
            favorites = json.loads(query.favorites)
            if clubid in favorites:
                return jsonify({"Error:" : "Already in favorites."}), 400
            else:
                favorites.append(clubid)
                query.favorites = json.dumps(favorites)
                clubquery.favorites += 1
                db.session.commit()
                return {}
    else: 
        return jsonify({"Error:" : "User Not Authenticated."}), 400

@app.route('/api/modify', methods = ['POST'])
def modify():
    clubid = request.form.get("clubid")
    field = request.form.get("field")
    value = request.form.get("value")
    query = Club.query.filter_by(code = clubid)
    if str(field) in ["description", "name"] and query.one_or_none() is not None:
        query.update({field: value})
        db.session.commit()
        return {}
    elif str(field) == "tags":
        query.update({field: json.dumps(value)})
        db.session.commit()
        return {}
    else: 
        return jsonify({"Error:" : "Invalid field to modify."})

@app.route('/api/tags')
def tags():
    tagdict = {}
    query = Club.query.all()
    for i in query:
        taglist = json.loads(i.tags)
        for tag in taglist:
            if tag in tagdict.keys():
                tagdict[tag] += 1
            else:
                tagdict[tag] = 1
    return jsonify(tagdict)
    
@app.route('/api/adduser', methods = ['POST'])
def adduser():
    salt = bcrypt.gensalt()
    userid = request.form.get("id")
    username = request.form.get("username")
    name = request.form.get("name")
    grad = request.form.get("grad")
    major = request.form.get("major")
    email = request.form.get("email")
    hash = bcrypt.hashpw(request.form.get("password").encode(), salt)
    # lastlogin = datetime.now(),
    # favorites = json.dumps([])
    query = User.query.filter_by(id = userid).one_or_none()
    query2 = User.query.filter_by(username = username).one_or_none()
    if query is not None and query2 is not None:
        return jsonify({"Error": "User already exists with that PennID or username."}), 400
    user = User(id = userid, username = username, name = name, grad = grad, major = major, hash = hash, salt = salt, email = email)
    db.session.add(user)
    db.session.commit()
    return {}

@app.route('/api/addtag', methods = ['POST'])
def addtag():
    clubid = request.form.get("clubid")
    tag = request.form.get("tag")
    query = Club.query.filter_by(code = clubid).one_or_none()
    if query is not None:
        l = json.loads(query.tags)
        if tag in l:
            return jsonify({"Error:" : "Tag already in club."}), 400
        l.append(tag)
        query.tags = json.dumps(l)
        db.session.commit()
        return {}
    else:
        return jsonify({"Error:" : "Club does not exist."}), 400

@app.route('/api/login', methods = ['POST'])
def login():
    username = request.form.get("username")
    passwd = request.form.get("password")
    query = User.query.filter_by(username = username).one_or_none() 
    salt = bytes(query.salt)
    if query is not None and str(bcrypt.hashpw(passwd.encode(), salt)) == str(query.hash):
          login_user(query, remember=False)
          return {}
    else:
        return jsonify({"Error:" : "Incorrect password, or user does not exist."}), 400

from flask_login import logout_user 
@app.route('/api/logout', methods = ['POST'])
@login_required
def logout():
    logout_user()
    return {}

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).one_or_none()

from werkzeug.utils import secure_filename

# Challenge 3: File Upload
@app.route('/api/upload', methods = ['POST'])
def upload():
    f = request.files['file']
    clubid = request.form.get("clubid")
    query = Club.query.filter_by(code = clubid).one_or_none()
    if query is not None:
        f.save(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))
        l = json.loads(query.files)
        l.append(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))
        query.files = json.dumps(l)
        db.session.commit()
    return {}

# Unit tests! Mainly tests the POST routes as the GET routes are viewable via browser
if __name__ == '__main__':
    app.secret_key = "super secret key"
    with app.test_client() as test_client:
        response = test_client.post('/api/login', data = dict(username = "josh", password = "password"))
        print(response)
        response = test_client.post('/api/favorite', data = dict(id = 31394502, clubid = "pppjo"))
        print(response)
        response = test_client.post('/api/add', data = dict(code = "ecfc", name = "Eric Cao's Fantastic Club", 
        description = "This is a club that I made for testing!", tags = ["Pre-Professional", "Technology"]))
        print(response)
        response = test_client.get('/api/search', query_string = dict(query = "cao"))
        print(response.data)
        response = test_client.post('/api/modify', data = dict(field = "description", clubid = "ecfc", value = "This is a changed Description."))
        print(response)
        response = test_client.post('/api/addtag', data = dict(clubid = "ecfc", tag = "Athletics"))
        print(response)
        response = test_client.get('/api/search', query_string = dict(query = "cao"))
        print(response.data)
        response = test_client.post('/api/adduser', data = dict(id = 12345678, username = "ecao", name = "Eric Cao", grad = 2029, major = "Mathematics", password = "PennLabsCool2", email = "ecao22@seas.upenn.edu"))
        print(response)
        response = test_client.get('/api/profile', query_string = dict(username = "ecao"))
        print(response.data)
        response = test_client.post('/api/logout')
        print(response)
        response = test_client.post('/api/favorite', data = dict(id = 31394502, clubid = "pppjo"))
        print(response)
        response = test_client.post('/api/upload', data = dict(file = (open("file.txt", 'rb'), "file.txt"), clubid = "ecfc"))
        print(response)
        response = test_client.get('/api/clubs')
        print(response.data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')