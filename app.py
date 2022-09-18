from cmath import e
import bcrypt
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE}"
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
    parsed = [i.to_dict() for i in query]
    return jsonify(parsed)

@app.route('/api/add', methods = ['POST'])
def add():
    # code = db.Column(db.String(20), unique=True, nullable=False, primary_key = True)
    # name = db.Column(db.String(60), nullable=False)
    # description = db.Column(db.Text(), nullable=False)
    # tags = db.Column(db.Text())

    code = request.form.get("code")
    name = request.form.get("name")
    description = request.form.get("description")   
    print("Before tags")
    tags = json.dumps(request.form.get("tags"))
    print("Made it through tags")
    query = Club.query.filter_by(code = code).one_or_none()
    if query is not None:
        print("Already exists")
        return {}
    club = Club(code = code,
        name = name,
        description = description,
        tags = tags)
    db.session.add(club)
    db.session.commit()
    print("Commited")
    return {}

from flask_login import login_required, current_user

@app.route('/api/favorite', methods = ['POST'])
# @login_required
def favorite():
    print("In Favorite.")
    id = request.form.get("id")
    clubid = request.form.get("clubid")
    query = User.query.filter_by(id = id).one_or_none()
    clubquery = Club.query.filter_by(code = clubid).one_or_none()

    loginip = request.remote_addr
    if query == current_user:
        print("Current User.")
        if query is not None and clubquery is not None:
            favorites = json.loads(query.favorites)
            if clubid in favorites:
                print("already in favorites")
                return {}
            else:
                print("Working.")
                print(favorites)
                favorites.append(clubid)
                query.favorites = json.dumps(favorites)
                clubquery.favorites += 1
                db.session.commit()
                return {}
    else: 
        return 401

@app.route('/api/modify', methods = ['POST'])
def modify():
    clubid = request.form.get("id")
    field = request.form.get("field")
    value = request.form.get("value")
    query = Club.query.filter_by(code = clubid).one_or_none()
    if field in ["description", "name", "tags"] and query is not None:
        query.update({field: value})
        db.session.commit()
        return {}
    else: 
        return {}

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
    id = request.json.get("id")
    username = request.json.get("username"),
    name = request.json.get("name"),
    grad = request.json.get("grad"),
    major = request.json.get("major"),
    key = bcrypt.hashpw(request.json.get("password"), salt),
    # lastlogin = datetime.now(),
    favorites = json.dump({})

    user = User(id = id, username = username, name = name, grad = grad, major = major, key = key, salt = salt, favorites = favorites)
    db.session.add(user)
    db.session.commit()

@app.route('/api/login', methods = ['POST'])
def login():
    # loginip = request.remote_addr
    username = request.form.get("username")
    passwd = request.form.get("password")
    # username = "josh"
    # passwd = "password"
    print(username)
    query = User.query.filter_by(username = username).one_or_none() 
    salt = bytes(query.salt)
    print(str(bcrypt.hashpw(passwd.encode(), salt)))
    print(query.hash)
    if query is not None and str(bcrypt.hashpw(passwd.encode(), salt)) == str(query.hash):
          login_user(query, remember=False)
          print("Logged in.")
    #     query.is_authenticated = True
    #     query.auth_ip = loginip
          return {}
    else:
        print("Fail")

@app.route('/api/logout', methods = ['POST'])
def logout():
    loginip = request.remote_addr
    username = request.args.get("username")
    query = User.query.filter_by(username = username).one_or_none() 
    if query is not None and query.auth_ip == loginip:
        query.auth_ip = "0.0.0.0"
        query.is_authenticated = False
    else:
        return 401

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).one_or_none()

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
        print(response)
        response = test_client.post('/api/modify', data = dict(field = "description", clubid = "ecfc", value = "This is a changed Description."))
        print(response)


# if __name__ == '__main__':
#     app.run()