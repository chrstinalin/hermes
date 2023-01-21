from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sjkhdfhiuwer'

    from .views import views
    from .map import mapB
    from .about import aboutB
    from .contact import contactB

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(mapB, url_prefix='/')
    app.register_blueprint(aboutB, url_prefix='/')
    app.register_blueprint(contactB, url_prefix='/')

    return app

