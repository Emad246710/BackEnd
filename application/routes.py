from flask import request, render_template, make_response, jsonify, abort
from flask import current_app as app
from flask_login import login_required, logout_user, current_user, login_user
# from werkzeug.security import generate_password_hash, check_password_hash
# import uuid
from .models import User, UserSchema, sqlalc




@app.route('/login', methods=[ 'POST'])
def login():
    data = request.get_json()

    if  not (data['username'] and data['password']):
        return {'errMsg':'Missing username or password! Please log in again.'}, 403

    user = User.query.filter(User.username == data['username']).one_or_none()
    if (user is None) or (user.password != data['password']):
        return {'errMsg':'Invalid username or password! Please log in again.'}, 403

    login_user(user)
    return  {'Msg':'Logged in successfully!'}, 201 

@app.route('/logout', methods=[ 'GET'])
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return  {'Msg':'Logged out successfully!'}, 201 



@app.route('/', methods=['GET'])
def home():
    """Create a user via query string parameters."""
    users = User.query.all()
    print(users)
    return {"data": [
        {"username": u.username, "password": u.password, "notes":
         [
            {"id": n.id, "content": n.content, "createdOn": n.createdOn,
                "priority": n.priority, "categoryId": n.categoryId}
            for n in u.notes
            ]
         }
        for u in users
    ]}


@app.route('/users', methods=['GET'])
@login_required
def user_all():
    """
    This function responds to a request for GET /api/users
    with the complete lists of user
    :return:        JSON string of list of user
    """
    users = User.query.all()
    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = user_schema.dump(users)
    print('***********************************************************')
    print(data)
    print('***********************************************************')
    return jsonify(data)


@app.route('/users/<id>', methods=['GET'])
@login_required
def user_one(id):
    """
    This function responds to a request for GET /api/users/{id}
    with JUST one matching user
    :param id:      id of the user to find
    :return:        User matching id
    """
    # Build the initial query
    user = User.query.filter(User.id == 1).one_or_none()
    print(id)

    if user is not None:
        # Serialize the data for the response
        user_schema = UserSchema()
        # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
        data = user_schema.dump(user)
        print('***********************************************************')
        print(data)
        print('***********************************************************')
        return jsonify(data)
    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"User not found for id: {id}")


@app.route('/register', methods=[ 'POST'])
def signup_user():
    data = request.get_json()

    is_user_exists = (User.query.filter(User.username == data['username']).first()) is not None 
    if is_user_exists:
        return ({'msg:': f"User with username: {data['username']} is already registered!"}) , 409

    user_schema = UserSchema()
    new_user = user_schema.load(data, session=sqlalc.session)
    # Add the user to the database
    sqlalc.session.add(new_user)
    sqlalc.session.commit()
    # flask_login: login_user() is a method that comes from the flask_login package that does exactly what it says
    login_user(user)  

    return  {'Msg':'Registered successfully!'}, 201 
