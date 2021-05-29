from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_cors import CORS
from flask_principal import  Principal, RoleNeed, UserNeed, identity_loaded, Permission



# Globally accessible db and ma
# Note the presence of (db and ma) and its location: this our database object being set as a global variable outside of create_app(). Inside of create_app(), on the other hand, contains the line db.init_app(app). Even though we've set our db object globally, this means nothing until we initialize it after creating our application. We accomplish this by calling init_app() within create_app(), 
sqlalc = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

# we might be using this feature"admin". but not yet to  be decided
# This must be initialized after login_manager
principals = Principal()
admin_permission = Permission(RoleNeed('yeh!_admin'))


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

    # This must be initialized after login_manager
    principals.init_app(app)

    # CORS(app )
    CORS(app, supports_credentials=True, ) # defualt origins='*'
    # CORS(app, origins='^http.*' , supports_credentials=True)
    # CORS(app, origins='http://localhost:3000' , supports_credentials=True)



    with app.app_context():
        # Include our Routes
        from . import auth
        from . import routes
        # from . import auth

        # flask_principal
        @identity_loaded.connect_via(app)
        def on_identity_loaded(sender, identity):
            # Set the identity user object
            identity.user = current_user
            # Add the UserNeed to the identity
            if hasattr(current_user, 'id'):
                identity.provides.add(UserNeed(current_user.id))

            print('********************************************************************')
            print('******identity_loaded.connect_via*************')
            print('********************************************************************')

            # Just for testing we will give user with "id=1", admin role
            # But the user table in the db should have a "role" column and depending on the value of that column we can set the "RoleNeed" value 
            if hasattr(current_user, 'id'): # This to ensure that the user is not instance of AnonymousUserMixin, which is the case if the user didn't logged in OR after logout
                if current_user.id == 1:
                    identity.provides.add(RoleNeed('yeh!_admin'))
                else:
                    identity.provides.add(RoleNeed('not_admin'))

        # Register Blueprints
        # app.register_blueprint(auth.auth_bp)
        # app.register_blueprint(admin.admin_bp)

        return app