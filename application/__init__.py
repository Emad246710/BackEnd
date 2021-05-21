from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

from flask_cors import CORS


# Globally accessible db and ma
# Note the presence of (db and ma) and its location: this our database object being set as a global variable outside of create_app(). Inside of create_app(), on the other hand, contains the line db.init_app(app). Even though we've set our db object globally, this means nothing until we initialize it after creating our application. We accomplish this by calling init_app() within create_app(), 
sqlalc = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')


    # Initialize Plugins,, Bind db to Flask  instead of "db = SQLAlchemy(app)"
    # After the app object is created, we then "initialize" those plugins we mentioned earlier. Initializing a plugin registers a plugin with our Flask app.
    # Setting db as global variables outside of init_app() makes it globally accessible to other parts of our application
    sqlalc.init_app(app)
    ma.init_app(app)
    login_manager.init_app(app)

    # CORS(app )
    CORS(app, supports_credentials=True, ) # defualt origins='*'
    # CORS(app, origins='^http.*' , supports_credentials=True)
    # CORS(app, origins='http://localhost:3000' , supports_credentials=True)



    with app.app_context():
        # Include our Routes
        from . import routes
        # Auth
        from . import auth

        # Register Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        return app