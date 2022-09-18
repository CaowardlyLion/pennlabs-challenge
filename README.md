# Penn Labs Backend Challenge

## Documentation

To begin, two models are made, one titled User and one titled Club. 

Club contains a field for the code, name, description, and tags, as well as a column called "favorites" that keeps track of the number of times the club has been favorited. 
User has columns for a PennID, username, name, graduation year, major, email, and favorites, as well as a salt and hash column used later for authentication.
Both classes have to_dict() methods that are called upon in the application's various GET routes.
Note: Both club tags and user favorites are stored as json dumped text.

In bootstrap.py:
create_user() does exactly as told, creating a user called josh with a terrible password. At least it's encrypted. A random salt is generated and hashed alongside the inputted password.
load_data() loops through clubs.json, adding each one to the database via Club. We also dump the list of tags from each club.
 --> Challenge 1 is implemented, which scans for where the description, name, and tag data are in the website. 
 --> However, to generate codes, we turn the name of the club into an acronym; if such a code already exists, we append a number on the end until it is no longer a duplicate.

Outside libraries used are bcrypt for password encryption and bs4 and requests for web scraping.

In app.py:



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
