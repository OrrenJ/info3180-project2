"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import UserProfile
from forms import RegistrationForm, LoginForm
import json
import hashlib


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "POST" and form.validate_on_submit():
        return redirect(url_for('api_users_register'), code=307)

    flash_errors(form)
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        return redirect(url_for('api_users_login'), code=307)

    flash_errors(form)
    return render_template('login.html', form=form)

@app.route('/api/users/register', methods=["GET", "POST"])
def api_users_register():
    if request.method == "POST":

        if 'email' not in request.form \
        or 'name' not in request.form \
        or 'password' not in request.form \
        or 'age' not in request.form \
        or 'gender' not in request.form :
            output = { "error": True, "data": {}, "message": "Invalid request format" }
        else:
            email = request.form.get('email')
            name = request.form.get('name')
            password = request.form.get('password')
            hash_pass = hashlib.sha512(password).hexdigest()
            age = request.form.get('age')
            gender = request.form.get('gender')
            image = "avatar.jpg"

            existing = UserProfile.query.filter_by(email=email).all()

            # check if user exists
            if len(existing) > 0:
                output = { "error": True, "data": {}, "message": "Email address already in use" }
            else:
                # current time in milliseconds, guaranteed unique
                new_user = UserProfile(email, name, hash_pass, age, gender)
                db.session.add(new_user)
                db.session.commit()

                data =  { 
                            "user": {
                                "id": new_user.id,
                                "name": new_user.name,
                                "email": new_user.email,
                                "age": new_user.age,
                                "gender": new_user.gender,
                                "image": image
                            } 
                        }

                output = { "error": None, "data": data, "message": "Success" }
            # endif
        #endif
    else:
        output = { "error": True, "data": {}, "message": "Method not allowed" }

    return json.dumps(output, indent=4, sort_keys=True)

@app.route('/api/users/login', methods=["GET", "POST"])
def api_users_login():
    if request.method == "POST":

        if 'email' not in request.form \
        or 'password' not in request.form:
            output = { "error": True, "data": {}, "message": "Invalid request format" }
        else:
            email = request.form.get('email')
            password = request.form.get('password')
            hash_pass = hashlib.sha512(password).hexdigest()

            user = UserProfile.query.filter_by(email=email, password=hash_pass).first()

            if user is None:
                output = { "error": True, "data": {}, "message": "Incorrect username or password" }
            else:
                data =  {
                            "user": {
                                "email": user.email,
                                "name": user.name
                            }
                        }

                output = { "error": None, "data": data, "message": "Success" }

    else:
        output = { "error": True, "data": {}, "message": "Method not allowed" }

    return json.dumps(output, indent=4, sort_keys=True)

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
