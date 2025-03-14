import dash
import dash_core_components as dcc 
import dash_bootstrap_components as dbc
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required, LoginManager
import os
#import logging
from app.utils import get_db_url
from app.server import db, cache, create_database

from services.models import User 

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/tmp'
}


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = get_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("APP_SECRET", "secret")
    CACHE_CONFIG_APP = CACHE_CONFIG
    BASIC_AUTH_USER = os.environ.get('BASIC_AUTH_USER', 'cs')
    BASIC_AUTH_PASS = os.environ.get('BASIC_AUT_PASS', 'cs')


def create_app():
    server = Flask(__name__)
    config = BaseConfig()
    server.config.from_object(config)

    db.init_app(server)
    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app):
    # from app.layout import demo_layout
    # from app.layout import company_selector


    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    # Login layout:
    dashapp1 = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/login/',
                         assets_folder=get_root_path(__name__) + '/login/assets/',
                         meta_tags=[meta_viewport],
                         external_stylesheets=[dbc.themes.MINTY])
    with app.app_context():
        from app.layout import testUI
        from app.layout import login
        dashapp1.title = 'Login'
        dashapp1.layout = login.layout
        login.register_callbacks(dashapp1)   

    # Company compare layout:
    dashapp2 = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport],
                         external_stylesheets=[dbc.themes.MINTY])
    with app.app_context():
        dashapp2.title = 'Compare Companies'
        dashapp2.layout = testUI.layout
        testUI.register_callbacks(dashapp2)
    # _protect_dashviews(dashapp2)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    cache.init_app(server, config=BaseConfig.CACHE_CONFIG_APP)
    db.init_app(server)
    # with server.app_context():
    #     # create_database(db.engine)
    #     # db.create_all()
    # create_database(db)
    # login.init_app(server)
    # login.login_view = 'main.login'
    # migrate.init_app(server, db)
    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.login_view = '/login'

    # callback to reload the user object
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def register_blueprints(server):
    from app.handlers.handler_login import login_blueprint

    server.register_blueprint(login_blueprint)


if __name__ == '__main__':
    # service.load_pairs()
    server = create_app()
    server.run(debug=True, host='0.0.0.0')

    #logging.getLoggerClass().root.handlers[0].baseFilename
    #len(logging.getLoggerClass().root.handlers)

