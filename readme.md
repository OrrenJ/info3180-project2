INFO3180 - Project 2
====================

Group members
* Orren Joseph
* Andre Boothe


Python Libraries Used
----------------------

Flask
Flask-WTF
Flask-SQLAlchemy
Flask-Migrate
Flask-Login
Flask-Mail
psycopg2
gunicorn
requests
beautifulsoup4


__init__.py
-----------

Ensure that the line `app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://[user]:[password]@localhost/[database]"` in __init__.py matches the credentials used for your database.