@app.route('/notes/<id>', methods=[ 'PUT'])
def update_note():


 """    user_data = {}
    if (data['username'] is not None):
        user_data['username'] = data['username']
    if (data['password'] is not None):
        # TODO hash  the password
        user_data['password'] = data['password'] """


  

    # turn the passed in user into a db object, IMPORTANT: body.id = null
    note_schema = NoteSchema()
    deserialize_data = note_schema.load(note_data, session=sqlalc.session)

    # Set the value of update.id which was null prev.
    deserialize_data.id = id
    print(f'Rcvd data, {deserialize_data}!')

    # merge the new object "update" into the old "existed_user" and commit it to the db
    sqlalc.session.merge(deserialize_data)
    sqlalc.session.commit()

    return  {'Msg':'Updated successfully!' , "useId" : id}, 201 



