from operator import and_
from flask import request,  jsonify
from flask import current_app as app
from marshmallow.fields import Method
from flask_login import login_required, logout_user, current_user, login_user
from .models import User, UserSchema, Note, NoteSchema, Category, CategorySchema

from werkzeug.security import generate_password_hash,  check_password_hash

from . import sqlalc

#   ----------------------------- login logout -----------------------------------
@app.route('/login', methods=[ 'POST'])
def login():
    data = request.get_json()

    req_fields = ["username", "password"]
    for key in req_fields:
        if not (key in data):
            return {'errMsg':'Missing username or password! Please log in again.'}, 422

    user = get_user_with_username(data['username'])

    if (user is None) or ( not check_password_hash(user.password , data['password']) ):
        return {'errMsg':'Invalid username or password! Please log in again.'}, 401

    login_user(user)

    temp_user = user.__dict__
    user_without_password={}
    user_without_password['username'] = temp_user['username']
    user_without_password['id'] = temp_user['id']

    return  {'Msg':'Logged in successfully!', 'current_user': user_without_password}, 201 



@app.route('/logout', methods=[ 'GET'])
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return  {'Msg':'Logged out successfully!'}, 201 


@app.route('/checkusername/<username>', methods=['GET'])
def is_valid_username(username):
    user = get_user_with_username(username)
    if user is not None:
        return ({'errMsg':f"User with username: {username} is already registered!"}) , 409
    return  {'Msg':f"The username: {username} is valid as a new username!"}, 201 
#   ------------------------------------------------------------------------------




@app.route('/', methods=['GET'])
@login_required
def home():
    """Create a user via query string parameters."""
    return "Project sdfsdfsdf  ", 200

#   -----------------------------      User    -----------------------------------

# @app.route('/users', methods=['GET'])
# @login_required
# def user_all():
#     """
#     This function responds to a request for GET /users
#     with the complete lists of user
#     :return:        JSON string of list of user
#     """
#     users = User.query.all()
#     # Serialize the data for the response
#     user_schema = UserSchema(many=True)
#     # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
#     data = user_schema.dump(users)
#     print('***********************************************************')
#     print(data)
#     print('***********************************************************')
#     return jsonify(data) , 200
    

@app.route('/users/<id>', methods=['GET'])
@login_required
def user_one(id):
    """
    This function responds to a request for GET /users/{id}
    with JUST one matching user
    :param id:      id of the user to find
    :return:        User matching id
    """

    if not is_current_user_consist_with_given_userId(id):
        return {"errMsg" : f"User with id {current_user.id}, can't access the URI /users/{id}" } , 403

    user = get_user_with_id(id)
    if user is None:
        return ({'errMsg':f"User not found for id: {id}"}) , 409
    
    # Serialize the data for the response
    user_schema = UserSchema()
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = user_schema.dump(user)

    # Remove the password
    data.pop('password', None)
    user_without_password = data
    return  {'Msg':'Retrived successfully!', 'current_user': user_without_password}, 201 

def is_current_user_consist_with_given_userId(userId):
    return current_user.id == int(userId)

def get_user_with_id(userId):
    return User.query.filter(User.id == int(userId)).first()

def get_user_with_username(username):
    return User.query.filter(User.username == username).first()


@app.route('/users', methods=[ 'POST'])
def signup_user():
    user_data = request.get_json()

    # Since the value of 'id' is set as auto-increament, remove the 'id' key ,,IFEXISTS
    user_data.pop('id', None)

    # check that the not nullable fields exist
    req_fields = ["username", "password"]
    for key in req_fields:
        if not (key in user_data):
            return {'errMsg':'Missing username or password! Please try again.'}, 422

    is_user_exists = get_user_with_username(user_data['username']) is not None 
    if is_user_exists:
        return ({'errMsg': f"User with username: {user_data['username']} is already registered!"}) , 409

    hashed_pw = generate_password_hash(user_data['password'], "sha256")

    user_data['password'] = hashed_pw

    user_schema = UserSchema()
    new_user = user_schema.load(user_data, session=sqlalc.session)

    # Add the user to the database
    sqlalc.session.add(new_user)
    sqlalc.session.commit()
    # flask_login: login_user() is a method that comes from the flask_login package that does exactly what it says
    print(f'----------------------- new_user {new_user}') 
    login_user(new_user) 


    return  {'Msg':'Registered successfully!', 'id': new_user.id}, 201 



@app.route('/users/<id>', methods=[ 'PUT'])
@login_required
def update_user(id):

    if not is_current_user_consist_with_given_userId(id):
        return {"errMsg" : f"User with id {current_user.id}, can't access the URI /users/{id}" } , 403

    existed_user = get_user_with_id(id)
    if existed_user is None:
        return ({'errMsg': f"User with id: {id} is NOT registered!"}) , 409

    user_data = request.get_json()

    # remove the id attr if exists. 
    user_data.pop('id', None)

    # check that the not nullable fields exist
    req_fields = ["username", "password"]
    for key in req_fields:
        if not (key in user_data):
            return {'errMsg':'Missing some required fields! Please try again.'}, 422

    
    username_exsist = get_user_with_username(user_data['username'])
    is_valid_username = ( username_exsist is None) or ( username_exsist.id == current_user.id )
    if not is_valid_username:
        return ({'errMsg': f"User with usrename: {user_data['username']} is already registered!"}) , 409

    hashed_pw = generate_password_hash(user_data['password'], "sha256")
    user_data['password'] = hashed_pw


    # turn the passed in user into a db object, IMPORTANT: body.id = null
    user_schema = UserSchema()
    deserialize_data = user_schema.load(user_data, session=sqlalc.session)

    # Set the value of update.id which was null prev.
    deserialize_data.id = id

    # merge the new object "update" into the old "existed_user" and commit it to the db
    sqlalc.session.merge(deserialize_data)
    sqlalc.session.commit()

    return  {'Msg':'Updated successfully!' , "id" : id}, 201 


@app.route('/users/<id>', methods=[ 'DELETE'])
@login_required
def delete_user(id):
    if not is_current_user_consist_with_given_userId(id):
        return {"errMsg" : f"User with id {current_user.id}, can't access the URI /users/{id}" } , 403

    # Get the user requested
    user = get_user_with_id(id)

    # Did we find a user?
    if user is None:
       return  {'errMsg': f'User not found for id: {id}' }, 404 

    sqlalc.session.delete(user)
    sqlalc.session.commit()
    return  {'Msg':'deleted successfully!' , "id" : id}, 201 



#   ------------------------------------------------------------------------------



def get_note_with_id_and_current_user_id(noteId):
    return Note.query.filter(and_(Note.id == int(noteId) , Note.userId == current_user.id) ).first()

def owns_current_user_noteId(noteId):
    return (Note.query.filter(and_(Note.id == int(noteId) , Note.userId == current_user.id)).first()) is not None; 


#   -----------------------------      Note    -----------------------------------



@app.route('/users/<userId>/notes', methods=['GET'])
@login_required
def notes_all(userId):
    
    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/notes" } , 403

    notes =   Note.query.filter(Note.userId == current_user.id).all()

    #    Serialize the data for the response
    note_schema = NoteSchema(many=True)
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = note_schema.dump(notes)
    print('***********************************************************')
    print(data)
    print('***********************************************************')
    return jsonify(data)



#### create note


@app.route('/users/<userId>/notes', methods=[ 'POST'])
@login_required
def create_note(userId):

    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/notes" } , 403

    note_data = request.get_json()

    # Since the value of 'createdOn' is the dateTime of the server, remove the 'createdOn' key ,,IFEXISTS 
    note_data.pop('createdOn', None)
    # Since the value of 'id' is set as auto-increament, remove the 'id' key ,,IFEXISTS
    note_data.pop('id', None)

    # check that the not nullable fields exist
    req_fields = ["content", "priority", "userId", "categoryId"]
    for key in req_fields:
        if not (key in note_data):
            return {'errMsg':'Missing some required fields! Please try again.'}, 422

    if not is_current_user_consist_with_given_userId(note_data['userId']) :
        return ({'errMsg': f"The req-body contains a userId: {note_data['userId']}, but the current user has an id: {current_user.id}"}) , 409

    # Since each user has a specific categories we should check that the category with id: (note_data['categoryId]) belongs to the current_user
    if note_data['categoryId'] and (not owns_current_user_categoryId(note_data['categoryId'])):
        return ({'errMsg': f"The req-body contains a category with id: {note_data['categoryId']}, but the user with id: {current_user.id} does not has such categoryId!"}) , 409

    note_schema = NoteSchema()
    new_note = note_schema.load(note_data, session=sqlalc.session)

    # Add the user to the database
    sqlalc.session.add(new_note)
    sqlalc.session.commit()
    
    return  {'Msg':'Created successfully!' , "id" : new_note.id}, 201 


@app.route('/users/<userId>/notes/<id>', methods=[ 'PUT'])
@login_required
def update_note(userId , id):

    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/notes/.." } , 403

    # There is no need to check if the args revcd in the "request.get_json()" has the same structure as "model".
    # Becuase we using "unknown = EXCLUDE" to exclude any "unknown" properties.  
    note_data = request.get_json()

    # Since the value of 'createdOn' is the dateTime of the server, remove the 'createdOn' key ,,IFEXISTS 
    note_data.pop('createdOn', None)

    # check that the not nullable fields exist
    req_fields = ["content", "priority", "userId", "categoryId"]
    for key in req_fields:
        if not (key in note_data):
            return {'errMsg':'Missing some required fields! Please try again.'}, 422

    if not is_current_user_consist_with_given_userId(note_data['userId']) :
        return ({'errMsg': f"The req-body contains a userId: {note_data['userId']}, but the current user has an id: {current_user.id}"}) , 409

    # Since each user has a specific categories we should check that the category with id: (note_data['categoryId]) belongs to the current_user
    if note_data['categoryId'] and (not owns_current_user_categoryId(note_data['categoryId'])):
        return ({'errMsg': f"The req-body contains a category with id: {note_data['categoryId']}, but the user with id: {current_user.id} does not has such categoryId!"}) , 409

    existed_note = get_note_with_id_and_current_user_id(id)

    if existed_note is None :
        return ({'errMsg':f"The current user does not has a note with id: {id}"}) , 404

    # turn the passed in user into a db object, IMPORTANT: body.id = null
    note_schema = NoteSchema()
    deserialize_data = note_schema.load(note_data, session=sqlalc.session)

    # Set the value of update.id which was null prev.
    deserialize_data.id = existed_note.id

    # merge the new object "update" into the old "existed_user" and commit it to the db
    sqlalc.session.merge(deserialize_data)
    sqlalc.session.commit()

    return  {'Msg':'Updated successfully!' , "id" : id}, 201 


### read note_one


@app.route('/users/<userId>/notes/<id>', methods=['GET'])
@login_required
def note_one(userId, id):
   
    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/notes/.." } , 403

    note = get_note_with_id_and_current_user_id(id)

    if note is None:
        return ({'errMsg':f"The current user does not has a note with id: {id}"}) , 404

    # Serialize the data for the response
    note_schema = NoteSchema()
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = note_schema.dump(note)
    return jsonify(data), 201



#### delete note

@app.route('/users/<userId>/notes/<id>', methods=[ 'DELETE'])
@login_required
def delete_note(userId, id):

    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/notes/.." } , 403

    note = get_note_with_id_and_current_user_id(id)

    if note is None:
        return ({'errMsg':f"The current user does not has a note with id: {id}"}) , 404

    sqlalc.session.delete(note)
    sqlalc.session.commit()
    return  {'Msg':'deleted successfully!' , "id" : id}, 201 









#   ------------------------------------------------------------------------------



def get_category_with_id_and_current_user_id(categoryId):
    return Category.query.filter(and_(Category.id == int(categoryId)  , Category.userId == current_user.id)).first()

def get_category_with_type_and_current_user_id(type):
    return Category.query.filter(and_(Category.type == type , Category.userId == current_user.id)).first()

def owns_current_user_categoryType(type):
    return Category.query.filter(and_(Category.type == type , Category.userId == current_user.id)).first() is not None

def owns_current_user_categoryId(categoryId):
    return Category.query.filter(and_(Category.id == int(categoryId) , Category.userId == current_user.id)).first() is not None

#   -----------------------------      Category    -----------------------------------


@app.route('/users/<userId>/categories', methods=['GET'])
@login_required
def user_categories_all(userId):
    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/categories" } , 403

    categories = Category.query.filter(Category.userId == int(userId)).all()
    #    Serialize the data for the response
    category_schema = CategorySchema(many=True)
   # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = category_schema.dump(categories)

    return jsonify(data)



### create_category
@app.route('/users/<userId>/categories', methods=[ 'POST'])
@login_required
def create_category(userId):
    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/categories" } , 403

    category_data = request.get_json()

    # Since the value of 'id' is set as auto-increament, remove the 'id' key ,,IFEXISTS
    category_data.pop('id', None)

    # check that the not nullable fields exist
    req_fields = ["type" , "userId"] 
    for key in req_fields:
        if not (key in category_data):
            return {'errMsg':'Missing some required fields! Please try again.'}, 422

    if not is_current_user_consist_with_given_userId(category_data['userId']) :
        return ({'errMsg': f"The req-body contains a userId: {category_data['userId']}, but the current user has an id: {current_user.id}"}) , 409

    valid_type = (get_category_with_type_and_current_user_id(category_data['type'])) is not None 
    if valid_type:
        return ({'errMsg': f"Category with type: {category_data['type']} is already registered!"}) , 409

    category_schema = CategorySchema()
    new_category = category_schema.load(category_data, session=sqlalc.session)

    # Add the user to the database
    sqlalc.session.add(new_category)
    sqlalc.session.commit()
    
    return  {'Msg':'Created successfully!' , "id" : new_category.id}, 201 


@app.route('/users/<userId>/categories/<id>', methods=['GET'])
@login_required
def category_one(userId , id):

    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/categories/.." } , 403

    category = get_category_with_id_and_current_user_id(id)

    if category is  None:
        return ({'errMsg':f"The current user does not has a category with id: {id}"}) , 404

    # Serialize the data for the response
    category_schema = CategorySchema()
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = category_schema.dump(category)
    return jsonify(data), 201



### update_category

@app.route('/users/<userId>/categories/<id>', methods=[ 'PUT'])
@login_required
def update_category(userId, id):
    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/categories/.." } , 403

    # There is no need to check if the args revcd in the "request.get_json()" has the same structure as "model".
    # Becuase we using "unknown = EXCLUDE" to exclude any "unknown" properties.  
    category_data = request.get_json()

    # check that the not nullable fields exist
    req_fields = ["type" , "userId"] 
    for key in req_fields:
        if not (key in category_data):
            return {'errMsg':'Missing some required fields! Please try again.'}, 422

    if not is_current_user_consist_with_given_userId(category_data['userId']) :
        return ({'errMsg': f"The req-body contains a userId: {category_data['userId']}, but the current user has an id: {current_user.id}"}) , 409


    existed_category = get_category_with_id_and_current_user_id(id)

    if existed_category is  None:
        return ({'errMsg':f"The current user does not has a category with id: {id}"}) , 404

    type_exsist = get_category_with_type_and_current_user_id(category_data['type'])
    #  valid if 1-doesNotExisit 2-it's the same type as before 3- this user does not has this type  
    is_valid_type = ( type_exsist is None) or ( type_exsist.id == int(id)) 
    if not is_valid_type:
        return ({'errMsg': f"Category with type: {category_data['type']} is already registered!"}) , 409

    # turn the passed in user into a db object, IMPORTANT: body.id = null
    category_schema = CategorySchema()
    deserialize_data = category_schema.load(category_data, session=sqlalc.session)

    # Set the value of update.id which was null prev.
    deserialize_data.id = id

    # merge the new object "update" into the old "existed_user" and commit it to the db
    sqlalc.session.merge(deserialize_data)
    sqlalc.session.commit()

    return  {'Msg':'Updated successfully!' , "id" : id}, 201 


### delete_category

@app.route('/users/<userId>/categories/<id>', methods=[ 'DELETE'])
@login_required
def delete_category(userId,id):

    if not is_current_user_consist_with_given_userId(userId):
        return {"errMsg" : f"User with id {current_user.id} can't access the URI /users/{userId}/categories/.." } , 403

    category = get_category_with_id_and_current_user_id(id)

    if category is None:
        return ({'errMsg':f"The current user does not has a category with id: {id}"}) , 404

    sqlalc.session.delete(category)
    sqlalc.session.commit()
    return  {'Msg':'deleted successfully!' , "id" : id}, 201 
