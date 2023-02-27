# Diginote
A simple django application for note taking.

## Features

- User authentication: Users should be able to sign up, log in, and log out.
- Note creation: Users should be able to create new notes by entering a title and content.
- Note listing: Users should be able to see a list of all their notes on a single page.
- Note detail view: Users should be able to click on a note in the list to view its title and content.
- Note editing: Users should be able to edit the title and content of a note.
- Note deletion: Users should be able to delete a note.
- User-specific data: Each user should only be able to see and modify their own notes.
- Filtering: Users should be able to filter notes by title using a search bar.
- Testing: Write unit tests for at least two of the core application features, such as note creation or editing. The tests should cover both positive and negative scenarios and demonstrate the correct functioning of the application.

## Usage

### Virtual ENV

1. Clone the repo
```
git clone git@github.com:viirak/diginote.git
```
2. Go into the folder
```
cd diginote
```
3. Create a new virtual environment
```
python3 -m venv .venv
```
4. Activate the virtual environment
```
source .venv/bin/activate
```
5. Migrate the database schema
```
python manage.py migrate
```
6. Run the application
```
python manage.py runserver
```
You should be able to access the application at:
http://0.0.0.0:8000/

### Docker

Make sure you have Docker running on your machine.

1. Clone this repo

```
git clone git@github.com:viirak/diginote.git
```
3. Run docker, build container and run
```
docker-compose build
```
```
docker-compose up
```

The development server should be started.
```
Starting development server at http://0.0.0.0:8000/
```

You should be able to access the application at:
http://0.0.0.0:8000/
