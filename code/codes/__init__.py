from codes.dashboard_app.dashbo import create_dash_app
from flask import Flask
from codes.dashboard_app.dashbo import create_dash_app

def creation_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='manani'

    
    
    from .home import home
    from .pagee import pagee
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(pagee, url_prefix='/')
    create_dash_app(app)

    return app