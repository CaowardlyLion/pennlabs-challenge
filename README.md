# Penn Labs Backend Challenge

## Documentation

To begin, two models are made, one titled User and one titled Club. 

Club contains a field for the code, name, description, and tags, as well as a column called "favorites" that keeps track of the number of times the club has been favorited. 
User has columns for a PennID, username, name, graduation year, major, email, and favorites, as well as a salt and hash column used later for authentication.
Both classes have to_dict() methods that are called upon in the application's various GET routes.
Note: Both club tags and user favorites are stored as json dumped text. This makes direct reads easier to decipher without outside code, and makes reading the tags/favorites back into lists in code much easier. 
It also allows one to add new tags seamlessly, without the need for new columns.

In bootstrap.py:
create_user() does exactly as told, creating a user called josh with a terrible password. At least it's encrypted. A random salt is generated and hashed alongside the inputted password.
load_data() loops through clubs.json, adding each one to the database via Club. We also dump the list of tags from each club.
 --> Challenge 1 is implemented, which scans for where the description, name, and tag data are in the website. 
 --> However, to generate codes, we turn the name of the club into an acronym; if such a code already exists, we append a number on the end until it is no longer a duplicate.

Outside libraries used are bcrypt for password encryption and bs4 and requests for web scraping.

In app.py:
Each of the routes are implemented like asked. 
There is an adduser route that is a signup for new users, a log-in route that utilizes flask-login, and a logout route to end.
The favorites route is only usable when the target user is the one that is currently logged in. Otherwise it throws a 400 error.
For the custom route, I added an "addtag" route that appends new tags onto existing ones for a certain club, instead of needing one to modify the entire tag section.
To do this, we read in the tag json for a certain club code query, load it into a list, apppend the new tag, then dump it back into the json.
--> Challenge 2 is also implemented here, via a test-client. It tests all the POST routes as well as a few GET routes. The other ones can be tested via web-browser!

Challenge 4: 
A docker image was created that runs the webapp. To do this, navigate to the pennlabs-challenge directory, and run:
 > docker build -t pennlabs-challenge --no-cache . 
 Once it finishes building, run:
 > docker run -p 5500:5000 pennlabs-challenge
This creates a docker container, which allows one to access the webapp (on the network) through 127.0.0.1:5500/api.

## Installation

1. Click the green "use this template" button to make your own copy of this repository, and clone it. Make sure to create a **private repository**.
2. Change directory into the cloned repository.
3. Install `pipenv`
   - `pip install --user --upgrade pipenv`
4. Install packages using `pipenv install`.

## File Structure

- `app.py`: Main file. Has configuration and setup at the top. Add your [URL routes](https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing) to this file!
- `models.py`: Model definitions for SQLAlchemy database models. Check out documentation on [declaring models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/) as well as the [SQLAlchemy quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#quickstart) for guidance
- `bootstrap.py`: Code for creating and populating your local database. You will be adding code in this file to load the provided `clubs.json` file into a database.

## Developing

0. Determine how to model the data contained within `clubs.json` and then complete `bootstrap.py`
1. Run `pipenv run python bootstrap.py` to create the database and populate it.
2. Use `pipenv run flask run` to run the project.
3. Follow the instructions [here](https://www.notion.so/pennlabs/Backend-Challenge-Fall-20-31461f3d91ad4f46adb844b1e112b100).
4. Document your work in this `README.md` file.

## Submitting

Follow the instructions on the Technical Challenge page for submission.

## Installing Additional Packages

Use any tools you think are relevant to the challenge! To install additional packages
run `pipenv install <package_name>` within the directory. Make sure to document your additions.
