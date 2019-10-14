from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import LoginForm, EditProfileForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime
from app import bokeh_plot
from app import bokeh_nba
from bokeh.embed import server_document
from tornado.ioloop import IOLoop
from app.nba_data.BokehPlot import modify_doc
from bokeh.server.server import Server


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for('edit_profile'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@app.route('/')
@app.route('/index')
def index():
    posts = [
        {
            'author': {'username': "John"},
            "body": "Beautiful day in Portland!"
        },
        {
            "author": {"username": "Susan"},
            "body": "The Avengers movie was so cool!"
        }

    ]

    return render_template("index.html", title="Home", posts=posts)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template("login.html", title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/bokeh')
def bokeh():
    return render_template('bokeh.html', plot_div=bokeh_plot.div, resources=bokeh_plot.resources, plot_script=bokeh_plot.script)




@app.route('/nba')
def nba_bokeh():
    return render_template('nba_bokeh.html', plot_div=bokeh_nba.div, resources=bokeh_nba.resources, plot_script=bokeh_nba.script)



def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    print("Here is modify doc: {}".format(modify_doc))
    try:
        server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
        server.start()
        server.io_loop.start()
    except Exception as e:
        print(e)


@app.route('/nba2', methods=['GET'])
def bkapp_page():
    from threading import Thread
    Thread(target=bk_worker).start()
    script = server_document('http://localhost:5006/bkapp')
    print(script)
    return render_template("embed.html", script=script, template="Flask")
