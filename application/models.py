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
        nullable=True,
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
    user = relationship("User",backref= backref("notes", cascade="all,delete"))  
    
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
        nullable=False
        )
    userId = sqlalc.Column(
        sqlalc.Integer, 
        sqlalc.ForeignKey('User.id'),    
        nullable=True # make it nullable ???
        ) 
    user = relationship("User",backref= backref("categories", cascade="all,delete"))  

    def __repr__(self):
        return '<Category id: {arg1},  tp: {arg2} ,  userId: {arg3} >'.format(arg1=self.id , arg2=self.type , arg3=self.userId)



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Optional: deserialize to model instances

        # Handling Unknown Fields: By default, load will raise a ValidationError if it encounters a key with no matching Field in the schema
        # This behavior can be modified with the unknown option,, which among other can accept 'EXCLUDE' which excludes unknown fields
        unknown = EXCLUDE


    
    notes = fields.Nested('NoteSchema', default=[], many=True,) 
    categories = fields.Nested('CategorySchema', default=[], many=True) 
    

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True

        # Handling Unknown Fields: By default, load will raise a ValidationError if it encounters a key with no matching Field in the schema
        # This behavior can be modified with the unknown option,, which among other can accept 'EXCLUDE' which excludes unknown fields
        unknown = EXCLUDE

        include_fk = True # IMPORTANT to enable this, in orde to Post Note with field userId and categoryId "necessary in usecase where Note can have these FK as null"
    # category = fields.Nested('CategorySchema',  many=False,  only=["type"])


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        # Handling Unknown Fields: By default, load will raise a ValidationError if it encounters a key with no matching Field in the schema
        # This behavior can be modified with the unknown option,, which among other can accept 'EXCLUDE' which excludes unknown fields
        unknown = EXCLUDE
        include_fk = True 
        
    id = ma.auto_field()
    type = ma.auto_field()
    # user = fields.Nested('UserSchema',  many=False, only=["id"]) 



