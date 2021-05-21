from flask import request, make_response, jsonify, abort,  g
from flask import current_app as app
import sqlite3
# from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash("Joe123")
# check_password_hash(hash,"Joe123")


def get_db():
    if not hasattr(g, "_database"):
        print("create connection")
        g._database = sqlite3.connect("database.db")
    return g._database


@app.route("/")
def index():
    return 'HomePage', 200

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
        cur = conn.cursor()
        username = request.json['username']
        password = request.json['password']

        try:
            sql = ("INSERT INTO users (username, passwordhash) VALUES (?,?)")
            cur.execute(sql, (username, password))
            conn.commit()
        except sqlite3.Error as err:
            print("Error: {}".format(err))
            cur.close()
            return abort( 409, f"The request could not be completed due to a conflict with the current state of the target resource")
        else:
            print("User {} created with id {}.".format(username, cur.lastrowid))
            cur.close()
            return make_response(f"User added!", 201)

if __name__ == "__main__":
    app.run()

    