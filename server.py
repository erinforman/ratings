"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/users/<user_id>')
def user_info(user_id):

    current_user = Rating.query.filter_by(user_id = user_id).options(db.joinedload('movie')).all()

    return render_template("user_info.html", current_user = current_user)


@app.route('/registration', methods=['GET'])
def new_user():

    return render_template("registration_form.html")

@app.route('/registration', methods=['POST'])
def check_user():

    email =  request.form.get("email")
    password =  request.form.get("password")

    user = User.query.filter_by(email = email).first()

    if user:
        return render_template("return_form.html")
    else:
        new_user = User(email = email, password = password) 
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

@app.route('/log-in', methods=['GET'])
def user_login():

    return render_template("login_form.html")

@app.route('/log-in', methods=['POST'])
def check_login():

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email = email).first()

    if user.password == password:
        session['user_login'] = user.user_id
        flash('You were successfully logged in')
        return redirect("/")
    else:
        flash('Incorrect password or user does not exist in our database!')
        return redirect("/log-in")

@app.route('/log-out')
def logout():
    session['user_login'] = {}
    flash('You were successfully logged out')
    return redirect("/")

# @app.route('/user-details')
# def user_deets():
#     return


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
