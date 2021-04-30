from flask import request, render_template, make_response, jsonify, abort, redirect, url_for, flash, session, g
from flask import current_app as app
import sqlite3


def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("database.db")
    return g._database


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        print("close connection")
        db.close()

def valid_login(username, password):
    """Checks if username-password combination is valid."""
    # user password data typically would be stored in a database
    conn = get_db()

    hash = get_hash_for_login(conn, username)
    # the generate a password hash use the line below:
    # generate_password_hash("rawPassword")
    if hash != None:
        return check_password_hash(hash, password)
    return False


@app.route("/login", methods=["POST"])
def login():
    if not valid_login(request.form["username"], request.form["password"]):
        abort(404)
    conn = get_db()
    user = get_user_by_name(conn,request.form["username"])
    user["addresses"] = get_user_addresses(conn, user["userid"])
    print(user)
    session["userid"] = user["userid"]
    return user

@app.route("/logout")
def logout():
    session.pop("userid")
    return redirect(url_for("index"))

@app.route("/")
def index():
    return app.send_static_file("index.html")



@app.route("/users", methods=["GET"])
def users():
    conn = get_db()
    conn.row_factory = dict_factory
    cur = conn.cursor()
    users = cur.execute('SELECT * FROM users;').fetchall()

   
    return jsonify(users)




def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route("/users", methods=["POST"])
def add_user1():
        conn = get_db()
        (username,password ) = request.json
        add_user(conn,"abudi1", generate_password_hash("Haaji123"))
        return make_response(f"User added!", 201)



if __name__ == "__main__":
    app.run()

    