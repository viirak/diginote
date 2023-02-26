# Diginote
A simple django application for note taking.

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
