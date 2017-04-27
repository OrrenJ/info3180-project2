"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import UserProfile, ItemProfile
from forms import RegistrationForm, LoginForm, WishlistAddForm
import json
import hashlib
import base64
from image_getter import get_images


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
        response = json.loads(api_users_register())
        if response.get('error') == None and response.get('message') == 'Success':
        	flash("Successfully registered new user", "success")
        else:
        	flash("Unable to add user", "danger")

    flash_errors(form)
    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        response = json.loads(api_users_login())
        if response.get('error') == None and response.get('message') == 'Success':
            data = response.get('data')
            user = data.get('user')
            email = user.get('email')
            # since emails are unique
            user = UserProfile.query.filter_by(email=email).first()
            login_user(user)
            next = request.args.get('next')

            authtoken = base64.b64encode("%s:%s" % (user.email, user.password))
            return redirect(url_for('wishlist_add'))

    flash_errors(form)
    return render_template('login.html', form=form)

@app.route('/wishlist/add', methods=["GET", "POST"])
@login_required
def wishlist_add():
    form = WishlistAddForm()

    if request.method == "POST" and form.validate_on_submit():
        response = json.loads(api_wishlist_add(current_user.id))
        if response.get('error') == None and response.get('message') == 'Success':
        	flash("Successfully added item to wishlist", "success")
        else:
        	flash("Unable to add item to wishlist", "danger")

    flash_errors(form)
    return render_template('wishlist_add.html', form=form)

@app.route('/wishlist', methods=["GET", "POST"])
@login_required
def wishlist():
	return render_template('get_wishlists.html')

@app.route('/users/<userid>/wishlist')
@login_required
def user_wishlist(userid):

	name = get_name(userid)

	return render_template('wishlist.html', name=name, userid=userid)

@app.route('/mywishlist')
@login_required
def my_wishlist():
	return render_template('my_wishlist.html')

@app.route('/api/users/register', methods=["POST"])
def api_users_register():

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

    return json.dumps(output, indent=4, sort_keys=True)

# route to display error if get
@app.route('/api/users/register', methods=["GET"])
def api_users_register_error():
    output = { "error": True, "data": {}, "message": "Method not allowed" }
    return json.dumps(output, indent=4, sort_keys=True)

@app.route('/api/users/login', methods=["POST"])
def api_users_login():

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

    return json.dumps(output, indent=4, sort_keys=True)

# route to display error if get
@app.route('/api/users/login', methods=["GET"])
def api_users_login_error():
    output = { "error": True, "data": {}, "message": "Method not allowed" }
    return json.dumps(output, indent=4, sort_keys=True)

@app.route('/api/users/<userid>/wishlist', methods=["POST"])
def api_wishlist_add(userid):

    auth = request.authorization
    email = auth.get('username')
    password = auth.get('password')

    user = UserProfile.query.filter_by(id=userid, email=email, password=password).first()

    if user is None:
        output = { "error": True, "data": {}, "message": "Authorization failure" }
    else:

        if 'title' not in request.form \
        or 'description' not in request.form \
        or 'url' not in request.form \
        or 'thumbnail_url' not in request.form:
            output = { "error": True, "data": {}, "message": "Invalid request format" }
        else:

            title = request.form.get('title')
            description = request.form.get('description')
            url = request.form.get('url')
            thumbnail_url = request.form.get('thumbnail_url')

            new_item = ItemProfile(userid, title, description, url, thumbnail_url)
            db.session.add(new_item)
            db.session.commit()
            
            data = {
                        "item": {
                            "id": new_item.id,
                            "title": new_item.title,
                            "description": new_item.description,
                            "url": new_item.url,
                            "thumbnail_url": new_item.thumbnail_url
                        }
                    }
            
            output = { "error": None, "data": data, "message": "Success" }
        
    return json.dumps(output, indent=4, sort_keys=True)

@app.route('/api/users/<userid>/wishlist', methods=["GET"])
def api_wishlist_get(userid):

	auth = request.authorization
	email = auth.get('username')
	password = auth.get('password')

	user = UserProfile.query.filter_by(email=email, password=password).first()

	if user is None:
		output = { "error": True, "data": {}, "message": "Authorization failure" }
	else:
		itemssql = ItemProfile.query.filter_by(userid=userid).all()

		items = []

		for i in itemssql:

			item = {
				"id": i.id,
				"title": i.title,
				"description": i.description,
				"url": i.url,
				"thumbnail_url": i.thumbnail_url
			}

			items.append(item)

		data = {
			"items": items
		}

		output = { "error": False, "data": data, "message": "Success" }

	return json.dumps(output, indent=4, sort_keys=True)

@app.route('/api/thumbnails', methods=["GET"])
def api_thumbnails():

    auth = request.authorization
    email = auth.get('username')
    password = auth.get('password')

    user = UserProfile.query.filter_by(email=email, password=password).first()

    if user is None:
        output = { "error": True, "data": {}, "message": "Authorization failure" }
    else:
        if 'url' not in request.args:
            output = { "error": True, "data": {}, "message": "Invalid request format" }
        else:

            data = {
                    "thumbnails": get_images(request.args.get('url'))
                }

            output =    { "error": None, "data": data, "message": "Success" }
    return json.dumps(output, indent=4, sort_keys=True)

# route to display error if post
@app.route('/api/thumbnails', methods=["POST"])
def api_thumbnails_error():
    output = { "error": True, "data": {}, "message": "Method not allowed" }
    return json.dumps(output, indent=4, sort_keys=True)

# API route used by front end (not in project requirements)
@app.route('/api/users', methods=["POST"])
def api_get_users():
	
    auth = request.authorization
    email = auth.get('username')
    password = auth.get('password')

    user = UserProfile.query.filter_by(email=email, password=password).first()

    if user is None:
    	output = { "error": True, "data": {}, "message": "Authoriztion failure" }
    else:
    	users = []
    	userssql = UserProfile.query.all()

    	for u in userssql:
    		users.append({ "id": u.id, "name": u.name })

    	data = {
    		"users": users
    	}

    	output = { "error": False, "data": data, "message": "Success" }
    
    return json.dumps(output, indent=4, sort_keys=True)

@app.route('/api/users/<userid>/wishlist/<itemid>', methods=["DELETE"])
def wishlist_item_delete(userid, itemid):

	auth = request.authorization
	email = auth.get('username')
	password = auth.get('password')

	user = UserProfile.query.filter_by(email=email, password=password).first()

	if user is None:
		output = { "error": True, "data": {}, "message": "Authoriztion failure" }
	else:
		ItemProfile.query.filter_by(id=itemid, userid=userid).delete()
		db.session.commit()

		output = { "error": False, "data": {}, "message": "Success" }

	return json.dumps(output, indent=4, sort_keys=True)

# get user name from id
def get_name(userid):
	
	user = UserProfile.query.filter_by(id=userid).first()

	if user is None:
		return "N/A"
	else:
		return user.name

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route("/logout")
@login_required
def logout():
    # Logout the user and end the session
    logout_user()
    flash('You have logged out.', 'danger')
    return redirect(url_for('home'))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

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
