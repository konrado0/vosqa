# vosqa
VOSQA is a fork of OSQA "Open Source Q&amp;A System" https://github.com/OSQA/osqa.
Its main features include:
- new visual (hence VOSQA) interface - with emphasis on images and convenient infinite scrolling,
- use of TinyMCE editor friendly to people not familiar with markdown,
- dynamic Javascript fields validation.  

It is based on Django and JQuery frameworks (tested with Django 1.7, JQuery 1.8 on Ubuntu 12.04/14.04).

Install instructions:
- install all necessary packages (you can use convenience scripts for Ubuntu setup12.sh or setup14.sh from tools directory, depending on your system)
- setup12.sh or setup14.sh scripts also create virtualenv with required packages, initialize it to run next python commands
- create local version of settings: 'cp settings_local.py.dist settings_local.py' and configure to your liking
- create and initialize database for project: 'python manage.py migrate'
- then run 'python manage.py collectstatic' to collect static files
- run test server with 'python manage.py runserver'
- first created user is automatically an admin
- included is Eclipse PyDev project and example nginx/uwsgi configuration.