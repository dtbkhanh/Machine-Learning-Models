from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

# from app.extensions import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.services.models import User
from app.server import db

login_blueprint = Blueprint('login_blueprint', __name__, template_folder='templates')


# https://flask.palletsprojects.com/en/1.1.x/blueprints/https://flask.palletsprojects.com/en/1.1.x/blueprints/
@login_blueprint.route('/')
def index():
    return redirect('/login')


@login_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('handler_login.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.usermail.data).first()
        # if user is None or not user.check_password(form.password.data):
        #     error = 'Invalid username or password'
        #     return render_template('login.html', form=form, error=error)
        #
        # # login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('login_blueprint.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@login_blueprint.route('/logout/')
# @login_required
def logout():
    logout_user()

    return redirect(url_for('handler_login.index'))


@login_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('handler_login.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # validate user already exist
        user = User.query.filter_by(user_mail=form.usermail.data).first()
        if user is None:
            user = User(user_mail=form.usermail.data, user_name=form.username.data)
            # user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login_blueprint.login', id=user.id))

    return render_template('register.html', title='Register', form=form)
