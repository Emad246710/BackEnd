#from marshmallow_sqlalchemy.schema.sqlalchemy_schema import auto_field
from re import T
from . import sqlalc ,ma
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, backref  
from marshmallow import fields  , EXCLUDE
from flask_login import UserMixin


class User(UserMixin,sqlalc.Model):
    __tablename__ = 'User'
    # __table_args__ = {'extend_existing': True}  => Specifies that a table wit hthis name already exists in the target database.  When this is set, your model will 
    #                    not override existing tables Thus, it is possible that the fields in your model might not match up with columns in your table.
    __table_args__ = {'extend_existing': True} 
    id = sqlalc.Column(
        sqlalc.Integer, 
        primary_key=True, 
        )
    username = sqlalc.Column(
        sqlalc.String(80), 
        unique=True, 
        nullable=False,
        )
    password = sqlalc.Column(
        sqlalc.String(80), 
        index=False,
        unique=False, 
        nullable=False
        )
    def __repr__(self):
        return '<User id:{arg0} usn: {arg1},  psw: {arg2} >'.format(arg0=self.id ,arg1=self.username , arg2=self.password)


class Note(sqlalc.Model):
    __tablename__ = 'Note'
    __table_args__ = {'extend_existing': True} 
    id = sqlalc.Column(
        sqlalc.Integer,
        primary_key=True
        )
    content = sqlalc.Column(
        sqlalc.String(400), 
        nullable=False
        )
    createdOn = sqlalc.Column( 
         sqlalc.String(80), 
        #sqlalc.DateTime, 
        default=datetime.now(timezone.utc).isoformat(),
        nullable=False  
        ) 
    priority = sqlalc.Column(
        sqlalc.Integer, 
        nullable=True,
        )
    userId = sqlalc.Column(
        sqlalc.Integer, 
        sqlalc.ForeignKey('User.id'),    
        nullable=False # make it nullable ???
        ) 
    user = relationship("User",backref="notes")             # <----------One to many  we will call this feild  
    # user = relationship(                                # <----------One to many  we will call this feild
    #     "User",
    #     backref="notes"
    #     cascade='all, delete, delete-orphan',
    #     single_parent=True,
    #     order_by='desc(Note.createdOn)'
    # )               
    categoryId = sqlalc.Column(
        sqlalc.Integer, 
        sqlalc.ForeignKey('Category.id'),    
        nullable=True  
        ) 

    category = relationship("Category", backref="notes")    # <----------One to many  we will call this feild 

    def __repr__(self):
        return '<Note id: {arg1},  tp: {arg2} >'.format(arg1=self.id , arg2=self.content)


class Category(sqlalc.Model):
    __tablename__ = 'Category'
    __table_args__ = {'extend_existing': True} 
    id = sqlalc.Column(
        sqlalc.Integer, 
        primary_key=True
        )
    type = sqlalc.Column(
        sqlalc.String(80), 
        unique=True,
        nullable=False
        )
    
    def __repr__(self):
        return '<Category id: {arg1},  tp: {arg2} >'.format(arg1=self.id , arg2=self.type)
    # returns <Category id: 1,  tp: type1 >


""" 
How to use  UserSchema :
    This is a serialization mechanizm using the Marshmallow package and its instance "ma" which is initiated in __init__.py file,
    Make sure to import "ma" from __init__.py by uncommenting "from . import ma"

    and UserSchema can be used as flws:
    @app.route('/', methods=['GET'])
    def user_records():
        users = User.query.all()
        user_schema = UserSchema(many=True)
        print(user_schema.dump(users))
        return jsonify(user_schema.dump(users))
"""
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Optional: deserialize to model instances
        # include_relationships = True

        # Handling Unknown Fields: By default, load will raise a ValidationError if it encounters a key with no matching Field in the schema
        # This behavior can be modified with the unknown option,, which among other can accept 'EXCLUDE' which excludes unknown fields
        unknown = EXCLUDE


    # username = ma.auto_field()
    # password = ma.auto_field()
    notes = fields.Nested('NoteSchema', default=[], many=True, exclude=("user",)) # NOTE that: "exclude" takes a collection of strings, hence the trailing coma.
    # # notes = ma.auto_field()

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        # include_relationships = True

        # Handling Unknown Fields: By default, load will raise a ValidationError if it encounters a key with no matching Field in the schema
        # This behavior can be modified with the unknown option,, which among other can accept 'EXCLUDE' which excludes unknown fields
        unknown = EXCLUDE

        include_fk = True # IMPORTANT to enable this, in orde to Post Note with field userId and categoryId "necessary in usecase where Note can have these FK as null"
    user = fields.Nested('UserSchema',  many=False, exclude=("notes",)) # NOTE that: "exclude" takes a collection of strings, hence the trailing coma.
    category = fields.Nested('CategorySchema',  many=False,  only=["type"])


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        # Handling Unknown Fields: By default, load will raise a ValidationError if it encounters a key with no matching Field in the schema
        # This behavior can be modified with the unknown option,, which among other can accept 'EXCLUDE' which excludes unknown fields
        unknown = EXCLUDE

    id = ma.auto_field()
    type = ma.auto_field()



# 
# The flwg sol is used to prevent the "infinite nested loop" between User and Note
# Instead of this use the   exclude=("user",)   and   exclude=("notes",) .... NOTE that: "exclude" takes a collection of strings, hence the trailing coma.
# 
# class NoteUserSchema(ma.SQLAlchemyAutoSchema):
#     """
#     This class is just like User BUT WITHOUT the "Note relation"
#     This class exists to get around a recursion issue
#     """
#     id = fields.Int()
#     username = fields.Str()
#     password = fields.Str()

# class UserNoteSchema(ma.SQLAlchemyAutoSchema):
#     """
#     This class is just like Note
#     This class exists  to get around a recursion issue
#     """
#     id = fields.Int()
#     content = fields.Str()
#     createdOn = fields.Str()
#     priority = fields.Int()
#     category = fields.Nested('CategorySchema',  many=False,  only=["type"])
