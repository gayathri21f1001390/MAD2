from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

# User Model

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True,primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True) # Email should be unique 
    password = Column(Text, nullable=False) 
    role = Column(Text, nullable=False, default="user") # Librarian or user   

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','password', 'role',)
user_schema = UserSchema()
        

# Section model

class Section(db.Model):
    __tablename__ = "section"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    create_id = Column(Integer, nullable=False)
    update_date = Column(DateTime, nullable=False)
    update_id = Column(Integer, nullable=False)


    def __init__(self, name, description, create_date, update_date, create_id, update_id):
        self.name = name
        self.description = description
        self.create_date = create_date
        self.create_id = create_id
        self.update_date = update_date
        self.update_id = update_id
    
class SectionSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','create_date', 'create_id', 'update_date', 'update_id')
section_schema = SectionSchema()
sections_schema = SectionSchema(many=True)

# Books model

class Book(db.Model):
    __tablename__ = "book"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    authors = Column(Text, nullable=False)
    book_path = Column(Text, nullable=False)
    section_id = Column(Integer, ForeignKey("section.id"), nullable=False)
    # section = relationship("Section",back_populates="books")

    def __init__(self, name, content, authors, book_path, section_id):
        self.name = name
        self.content = content
        self.authors = authors
        self.book_path = book_path
        self.section_id = section_id

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "content", "authors","book_path","section_id")
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# User Book Model

class UserBook(db.Model):
    __tablename__ = "user_book"
    id = Column(Integer, primary_key = True, autoincrement = True )
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    book_id = Column(Integer, ForeignKey("book.id"), nullable = False)
    request_date = Column(DateTime, nullable = False)
    issue_date = Column(DateTime)
    due_date = Column(DateTime)
    return_date = Column(DateTime)
    revoke_date = Column(DateTime)
    status = Column(Text)
    
    def __init__(self, user_id, book_id, request_date, issue_date, due_date, return_date, revoke_date, status):
        self.user_id = user_id
        self.book_id = book_id
        self.request_date = request_date
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date
        self.revoke_date = revoke_date
        self.status = status

class UserBookSchema(ma.Schema):
    class Meta:
        fields = ("id","user_id", "book_id", "issue_date", "request_date","due_date","return_date", "revoke_date","status")
user_book_schema = UserBookSchema()
user_books_schema = UserBookSchema(many=True)