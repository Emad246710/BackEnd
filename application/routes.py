from operator import and_
from flask import request,  jsonify
from flask import current_app as app
from marshmallow.fields import Method
from flask_login import login_required, logout_user, current_user, login_user
# from werkzeug.security import generate_password_hash, check_password_hash
# import uuid
from .models import User, UserSchema, Note, NoteSchema, Category, CategorySchema

from . import sqlalc

#   ----------------------------- login logout -----------------------------------
@app.route('/login', methods=[ 'POST'])
def login():
    data = request.get_json()

    req_fields = ["username", "password"]
    for key in req_fields:
        if not (key in data):
            return {'errMsg':'Missing username or password! Please log in again.'}, 422

    user = User.query.filter(User.username == data['username']).one_or_none()
    if (user is None) or (user.password != data['password']):
        return {'errMsg':'Invalid username or password! Please log in again.'}, 401

    login_user(user)
    temp_user = user.__dict__

    user_without_password={}
    user_without_password['username'] = temp_user['username']
    user_without_password['id'] = temp_user['id']

    return  {'Msg':'Logged in successfully!', 'current_user': user_without_password}, 201 



@app.route('/logout', methods=[ 'GET'])
#@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return  {'Msg':'Logged out successfully!'}, 201 

#   ------------------------------------------------------------------------------




@app.route('/', methods=['GET'])
#@login_required
def home():
    """Create a user via query string parameters."""
    return "Project sdfsdfsdf  ", 200

#   -----------------------------      User    -----------------------------------

@app.route('/users', methods=['GET'])
#@login_required
def user_all():
    """
    This function responds to a request for GET /users
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
    return jsonify(data) , 200
    

@app.route('/users/<id>', methods=['GET'])
#@login_required
def user_one(id):
    """
    This function responds to a request for GET /users/{id}
    with JUST one matching user
    :param id:      id of the user to find
    :return:        User matching id
    """
    # Build the initial query
    user = User.query.filter(User.id == id).first()
    print(id)

    if user is not None:
        # Serialize the data for the response
        user_schema = UserSchema()
        # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
        data = user_schema.dump(user)


        user_without_password={}
        user_without_password['username'] = data['username']
        user_without_password['id'] = data['id']
        return  {'Msg':'Retrived successfully!', 'current_user': user_without_password}, 201 
    # Otherwise, nope, didn't find that user
    else:
        return ({'errMsg':f"User not found for id: {id}"}) , 409


@app.route('/users', methods=[ 'POST'])
def signup_user():
    user_data = request.get_json()
    # TODO hash  the password

    # check that the not nullable fields exist
    req_fields = ["username", "password"]
    for key in req_fields:
        if not (key in user_data):
            return {'errMsg':'Missing username or password! Please log in again.'}, 404

    is_user_exists = (User.query.filter(User.username == user_data['username']).first()) is not None 
    if is_user_exists:
        return ({'errMsg': f"User with username: {user_data['username']} is already registered!"}) , 409


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
#@login_required
def update_user(id):

    user_data = request.get_json()
    # TODO hash  the password


    existed_user = (User.query.filter(User.id == int(id)).first())
    if existed_user is None:
        return ({'errMsg': f"User with id: {id} is NOT registered!"}) , 409


    if (user_data['username'] is not None):
        username_exsist = User.query.filter(User.username == user_data['username'] ).first()
        is_valid_username = ( username_exsist is None) or ( username_exsist.id == int(id) )
        if not is_valid_username:
            return ({'errMsg': f"User with usrename: {user_data['username']} is already registered!"}) , 409

    # TODO hash  the password
    
    # if (user_data['password'] is  None):
    #     user_data['password'] = existed_user.password



    # turn the passed in user into a db object, IMPORTANT: body.id = null
    user_schema = UserSchema()
    deserialize_data = user_schema.load(user_data, session=sqlalc.session)

    # Set the value of update.id which was null prev.
    deserialize_data.id = id
    print(f'Rcvd data, {deserialize_data}!')

    # merge the new object "update" into the old "existed_user" and commit it to the db
    sqlalc.session.merge(deserialize_data)
    sqlalc.session.commit()

    return  {'Msg':'Updated successfully!' , "id" : id}, 201 


@app.route('/users/<id>', methods=[ 'DELETE'])
#@login_required
def delete_user(id):
    # Get the user requested
    user = User.query.filter(User.id == id).first()

    # Did we find a user?
    if user is None:
       return  {'errMsg': f'User not found for id: {id}' }, 404 

    sqlalc.session.delete(user)
    sqlalc.session.commit()
    return  {'Msg':'deleted successfully!' , "id" : id}, 201 



#   ------------------------------------------------------------------------------


#   -----------------------------      Note    -----------------------------------



@app.route('/users/<userId>/notes', methods=['GET'])
#@login_required
def notes_all(userId):
    notes =   Note.query.filter(Note.userId == int(userId)).all()

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
#@login_required
def create_note(userId):
    note_data = request.get_json()

    # Since the value of 'createdOn' is the dateTime of the server, remove the 'createdOn' key ,,IFEXISTS 
    note_data.pop('createdOn', None)

    # check that the not nullable fields exist
    req_fields = ["content", "priority", "userId", "categoryId"]
    for key in req_fields:
        if not (key in note_data):
            return {'errMsg':'Missing some required fields! Please try again.'}, 404
    
    if not int(note_data['userId']) == int(userId) :
        return ({'errMsg': f"The User with id {note_data['userId']}, can not cearte a Note on this route /users/{userId}/notes"}) , 409

    # Note that since each user has a specific categories we should check that the note_data['categoryId] belongs to the user with 'userId'

    note_schema = NoteSchema()
    new_note = note_schema.load(note_data, session=sqlalc.session)

    # Add the user to the database
    sqlalc.session.add(new_note)
    sqlalc.session.commit()
    
    return  {'Msg':'Created successfully!' , "id" : new_note.id}, 201 
    ###update_note

@app.route('/users/<userId>/notes/<id>', methods=[ 'PUT'])
#@login_required
def update_note(userId , id):
    note_data = request.get_json()
 # There is no need to check if the args revcd in the "request.get_json()" has the same structure as "model".
 # Becuase we using "" to exclude any "unknown" pproperties.  
    existed_note = Note.query.filter(Note.id == id).first()
    if existed_note is None :
        return ({'errMsg': f"Note with id: {id} is NOT registered!"}) , 409

    # Note that since each user has a specific categories we should check that the note_data['categoryId] belongs to the user with 'userId'

    if not existed_note.userId == int(userId) :
        return ({'errMsg': f"The User with id {userId}, can not edit the Note with id: {id}"}) , 409

    if not int(note_data['userId']) == int(userId) :
        return ({'errMsg': f"Can't set userId as {note_data['userId']}, becuase this Note {existed_note.id} belongs to The User with id {existed_note.userId}"}) , 409


    # turn the passed in user into a db object, IMPORTANT: body.id = null
    note_schema = NoteSchema()
    deserialize_data = note_schema.load(note_data, session=sqlalc.session)

    # Set the value of update.id which was null prev.
    deserialize_data.id = id

    # merge the new object "update" into the old "existed_user" and commit it to the db
    sqlalc.session.merge(deserialize_data)
    sqlalc.session.commit()

    return  {'Msg':'Updated successfully!' , "id" : id}, 201 


### read note_one


@app.route('/users/<userId>/notes/<id>', methods=['GET'])
#@login_required
def note_one(userId, id):
   
    # Build the initial query
    note = Note.query.filter(Note.id == id).first()
    print(id)

    if note is not None:
        if not note.userId == int(userId) :
            return ({'errMsg': f"The User with id {userId}, can not retrieve a Note with id: {id}"}) , 409

        # Serialize the data for the response
        note_schema = NoteSchema()
        # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
        data = note_schema.dump(note)
        print('***********************************************************')
        print(data)
        print('***********************************************************')
        return jsonify(data), 201
    # Otherwise, nope, didn't find that user
    else:
        return ({'errMsg':f"Note not found for id: {id}"}) , 409


#### delete note

@app.route('/users/<userId>/notes/<id>', methods=[ 'DELETE'])
#@login_required
def delete_note(userId, id):
    # Get the note requested
    note = Note.query.filter(Note.id == id).first()

    # Did we find a user?
    if note is None:
       return  {'errMsg': f'Note not found for id: {id}' }, 404 

    if not note.userId == int(userId) :
        return ({'errMsg': f"The User with id {userId}, can not delete the Note with id: {id}"}) , 409

    sqlalc.session.delete(note)
    sqlalc.session.commit()
    return  {'Msg':'deleted successfully!' , "id" : id}, 201 


# @app.route('/notes', methods=['GET'])
# #@login_required
# def notes_all():
#     notes = Note.query.all()
#     #    Serialize the data for the response
#     note_schema = NoteSchema(many=True)
#     # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
#     data = note_schema.dump(notes)
#     print('***********************************************************')
#     print(data)
#     print('***********************************************************')
#     return jsonify(data)



# #### create note


# @app.route('/notes', methods=[ 'POST'])
# #@login_required
# def create_note():
#     note_data = request.get_json()

#     # Since the value of 'createdOn' is the dateTime of the server, remove the 'createdOn' key ,,IFEXISTS 
#     note_data.pop('createdOn', None)

#     # check that the not nullable fields exist
#     req_fields = ["content", "priority", "userId", "categoryId"]
#     for key in req_fields:
#         if not (key in note_data):
#             return {'errMsg':'Missing some required fields! Please try again.'}, 404
    

#     note_schema = NoteSchema()
#     new_note = note_schema.load(note_data, session=sqlalc.session)

#     # Add the user to the database
#     sqlalc.session.add(new_note)
#     sqlalc.session.commit()
    
#     return  {'Msg':'Created successfully!' , "id" : new_note.id}, 201 
#     ###update_note

# @app.route('/notes/<id>', methods=[ 'PUT'])
# #@login_required
# def update_note(id):
#     note_data = request.get_json()
#  # There is no need to check if the args revcd in the "request.get_json()" has the same structure as "model".
#  # Becuase we using "" to exclude any "unknown" pproperties.  

#     existed_note = Note.query.filter(Note.id == id).first 
#     if existed_note is None :
#         return ({'errMsg': f"Note with id: {id} is NOT registered!"}) , 409


#     # turn the passed in user into a db object, IMPORTANT: body.id = null
#     note_schema = NoteSchema()
#     deserialize_data = note_schema.load(note_data, session=sqlalc.session)

#     # Set the value of update.id which was null prev.
#     deserialize_data.id = id

#     # merge the new object "update" into the old "existed_user" and commit it to the db
#     sqlalc.session.merge(deserialize_data)
#     sqlalc.session.commit()

#     return  {'Msg':'Updated successfully!' , "id" : id}, 201 


# ### read note_one


# @app.route('/notes/<id>', methods=['GET'])
# #@login_required
# def note_one(id):
   
#     # Build the initial query
#     note = Note.query.filter(Note.id == id).first()
#     print(id)

#     if note is not None:
#         # Serialize the data for the response
#         note_schema = NoteSchema()
#         # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
#         data = note_schema.dump(note)
#         print('***********************************************************')
#         print(data)
#         print('***********************************************************')
#         return jsonify(data), 201
#     # Otherwise, nope, didn't find that user
#     else:
#         return ({'errMsg':f"Note not found for id: {id}"}) , 409


# #### delete note

# @app.route('/notes/<id>', methods=[ 'DELETE'])
# #@login_required
# def delete_note(id):
#     # Get the note requested
#     note = Note.query.filter(Note.id == id).first()

#     # Did we find a user?
#     if note is None:
#        return  {'errMsg': f'Note not found for id: {id}' }, 404 

#     sqlalc.session.delete(note)
#     sqlalc.session.commit()
#     return  {'Msg':'deleted successfully!' , "id" : id}, 201 








#   ------------------------------------------------------------------------------


#   -----------------------------      Category    -----------------------------------


@app.route('/users/<userId>/categories', methods=['GET'])
#@login_required
def user_categories_all(userId):
    categories =   Category.query.filter(Category.userId == int(userId)).all()
    #    Serialize the data for the response
    category_schema = CategorySchema(many=True)
   # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = category_schema.dump(categories)
    print('***********************************************************')
    print(data)
    print('***********************************************************')
    return jsonify(data)



### create_category

@app.route('/users/<userId>/categories', methods=[ 'POST'])
#@login_required
def create_category(userId):
    category_data = request.get_json()

    # check that the not nullable fields exist
    req_fields = ["type" , "userId"] 
    for key in req_fields:
        if not (key in category_data):
            return {'errMsg':'Missing some required fields! Please try again.'}, 404

    
    valid_type = (Category.query.filter(and_(Category.type == category_data['type'] , Category.userId == int(userId))).first()) is not None 
    if valid_type:
        return ({'errMsg': f"Category with type: {category_data['type']} is already registered!"}) , 409

    if not int(category_data['userId']) == int(userId) :
        return ({'errMsg': f"The User with id {category_data['userId']}, can not cearte a Category on this route /users/{userId}/categories"}) , 409


    category_schema = CategorySchema()
    new_category = category_schema.load(category_data, session=sqlalc.session)

    # Add the user to the database
    sqlalc.session.add(new_category)
    sqlalc.session.commit()
    
    return  {'Msg':'Created successfully!' , "id" : new_category.id}, 201 


### category_read


@app.route('/users/<userId>/categories/<id>', methods=['GET'])
#@login_required
def category_one(userId , id):
   
    # Build the initial query
    category = Category.query.filter(Category.id == id).first()



    if category is not None:
        if not category.userId == int(userId) :
            return ({'errMsg': f"The User with id {userId}, can not retrieve a Category with id: {id}"}) , 409

        # Serialize the data for the response
        category_schema = CategorySchema()
        # is this wrong
        # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
        data = category_schema.dump(category)
        print('***********************************************************')
        print(data)
        print('***********************************************************')
        return jsonify(data), 201
    # Otherwise, nope, didn't find that user
    else:
        return ({'errMsg':f"Category not found for id: {id}"}) , 409



### update_category

@app.route('/users/<userId>/categories/<id>', methods=[ 'PUT'])
#@login_required
def update_category(userId, id):
    category_data = request.get_json()
 # There is no need to check if the args revcd in the "request.get_json()" has the same structure as "model".
 # Becuase we using "" to exclude any "unknown" pproperties.  
    print(category_data)

    existed_category = Category.query.filter(Category.id == id ).first()


    if existed_category is None :
        return ({'errMsg': f"Category with id: {id} is NOT registered!"}) , 409

    if not existed_category.userId == int(userId) :
        return ({'errMsg': f"The User with id {userId}, can not edit the Category with id: {id}"}) , 409

    if  (category_data['userId'] is not None):
        if   (int(category_data['userId']) != int(userId) ):
            return ({'errMsg': f"Can't set userId as {category_data['userId']}, becuase this category {existed_category.id} belongs to The User with id {existed_category.userId}"}) , 409

    if (category_data['type'] is not None):
        type_exsist = Category.query.filter(and_(Category.type == category_data['type'] , Category.userId == int(userId))).first()
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
#@login_required
def delete_category(userId,id):
    # Get the category requested
    category = Category.query.filter(Category.id == id).first()

    # Did we find a user?
    if category is None:
       return  {'errMsg': f'Category not found for id: {id}' }, 404 

    if not category.userId == int(userId) :
        return ({'errMsg': f"The User with id {userId}, can not delete the Category with id: {id}"}) , 409

    sqlalc.session.delete(category)
    sqlalc.session.commit()
    return  {'Msg':'deleted successfully!' , "id" : id}, 201 

















# @app.route('/categories', methods=['GET'])
# #@login_required
# def categories_all():
#     categories = Category.query.all()
#     #    Serialize the data for the response
#     category_schema = CategorySchema(many=True)
#    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
#     data = category_schema.dump(categories)
#     print('***********************************************************')
#     print(data)
#     print('***********************************************************')
#     return jsonify(data)



# ### create_category

# @app.route('/categories', methods=[ 'POST'])
# #@login_required
# def create_category():
#     category_data = request.get_json()

#     # check that the not nullable fields exist
#     req_fields = ["type"]
#     for key in req_fields:
#         if not (key in category_data):
#             return {'errMsg':'Missing some required fields! Please try again.'}, 404

    
#     is_type_exists = (Category.query.filter(Category.type == category_data['type']).first()) is not None 
#     if is_type_exists:
#         return ({'errMsg': f"Category with type: {category_data['type']} is already registered!"}) , 409


#     category_schema = CategorySchema()
#     new_category = category_schema.load(category_data, session=sqlalc.session)

#     # Add the user to the database
#     sqlalc.session.add(new_category)
#     sqlalc.session.commit()
    
#     return  {'Msg':'Created successfully!' , "id" : new_category.id}, 201 


# ### category_read


# @app.route('/categories/<id>', methods=['GET'])
# #@login_required
# def category_one(id):
   
#     # Build the initial query
#     category = Category.query.filter(Category.id == id).first()
#     print(id)

#     if category is not None:
#         # Serialize the data for the response
#         category_schema = CategorySchema()
#         # is this wrong
#         # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
#         data = category_schema.dump(category)
#         print('***********************************************************')
#         print(data)
#         print('***********************************************************')
#         return jsonify(data), 201
#     # Otherwise, nope, didn't find that user
#     else:
#         return ({'errMsg':f"Category not found for id: {id}"}) , 409



# ### update_category

# @app.route('/categories/<id>', methods=[ 'PUT'])
# #@login_required
# def update_category(id):
#     category_data = request.get_json()
#  # There is no need to check if the args revcd in the "request.get_json()" has the same structure as "model".
#  # Becuase we using "" to exclude any "unknown" pproperties.  

#     existed_category = Category.query.filter(Category.id == id).first()

#     if existed_category is None :
#         return ({'errMsg': f"Category with id: {id} is NOT registered!"}) , 409

#     if (category_data['type'] is not None):
#         type_exsist = Category.query.filter(Category.type == category_data['type'] ).first()
#         is_valid_type = ( type_exsist is None) or ( type_exsist.id == int(id) )
#         if not is_valid_type:
#             return ({'errMsg': f"Category with type: {category_data['type']} is already registered!"}) , 409

#     # turn the passed in user into a db object, IMPORTANT: body.id = null
#     category_schema = CategorySchema()
#     deserialize_data = category_schema.load(category_data, session=sqlalc.session)

#     # Set the value of update.id which was null prev.
#     deserialize_data.id = id

#     # merge the new object "update" into the old "existed_user" and commit it to the db
#     sqlalc.session.merge(deserialize_data)
#     sqlalc.session.commit()

#     return  {'Msg':'Updated successfully!' , "id" : id}, 201 


# ### delete_category

# @app.route('/categories/<id>', methods=[ 'DELETE'])
# #@login_required
# def delete_category(id):
#     # Get the category requested
#     category = Category.query.filter(Category.id == id).first()

#     # Did we find a user?
#     if category is None:
#        return  {'errMsg': f'Category not found for id: {id}' }, 404 

#     sqlalc.session.delete(category)
#     sqlalc.session.commit()
#     return  {'Msg':'deleted successfully!' , "id" : id}, 201 