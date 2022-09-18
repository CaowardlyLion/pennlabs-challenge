import json
import os
from app import db, DB_FILE
import bcrypt

def create_user():
    salt = bcrypt.gensalt()
    josh = User(id = 31394502,
    username = "josh",
    name = "Josh Doe",
    grad = 2026,
    major = "Computer Science",
    hash = bcrypt.hashpw(b"password", salt),
    salt = salt,
    favorites = json.dumps([]),
    email = "joshdoe@upenn.edu")
    
    db.session.add(josh)
    db.session.commit()
    
from models import *
import requests
from bs4 import BeautifulSoup

def load_data():
    file = open("clubs.json")
    data = json.load(file)
    for i in data:
        club = Club(code = i["code"],
        name = i["name"],
        description = i["description"],
        tags =  json.dumps(i["tags"]))
        db.session.add(club)       
    db.session.commit()

    # Challenge 1: Web Scraping
    url='https://ocwp.pennlabs.org/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text)

    section_data = soup.find('section', class_='section')

    if section_data is not None:
        clubs_data = section_data.find_all('div', class_='box')
        for club_data in clubs_data:
            club_name = club_data.find('strong', class_='club-name').get_text()
            club_desc = club_data.find('em').get_text()
            club_tag_data = club_data.find_all('span', class_='tag is-info is-rounded')
            s = club_name.split(" ")
            l = []
            for i in s:
                l.append(i[0].lower())
            club_code = "".join(l)
            club_tags = []
            for club_tag in club_tag_data:
                club_tags.append(club_tag.get_text())
            query = Club.query.filter_by(code = club_code).one_or_none()
            i = 0
            while query is not None:
                club_code = club_code + str(i)
                query = Club.query.filter_by(code = club_code).one_or_none()
            club = Club(code = club_code, name = club_name, description = club_desc, tags = json.dumps(club_tags))
            db.session.add(club)
    db.session.commit()



# No need to modify the below code.
if __name__ == '__main__':
    # Delete any existing database before bootstrapping a new one.
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    db.create_all()
    create_user()
    load_data()
    print("Bootstrap Done.")
