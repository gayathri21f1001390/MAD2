from flask import Flask, request, jsonify
from models import *
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies

app = Flask(__name__)
app.config.from_object(Config)
jwt=JWTManager(app)

# Init DB
db.init_app(app)
bcrypt = Bcrypt(app)

CORS(app, supports_credentials=True)

with app.app_context():
    db.create_all()
    
# Home route

@app.route("/")
def home():
    return "Welcome to Library Management System"

# New User Register Route

@app.route("/register", methods = ["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"message": "User exists"}), 409
 

    new_user = User(name=name, email=email, password=password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message" : "New User Created Successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : "Error Creating User"}), 500

# User Login

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    existing_user = User.query.filter_by(email=email).first()

    if not existing_user:
        return jsonify({"error": "User does not exist, register first"}), 404
    if not bcrypt.check_password_hash(existing_user.password,password):
        return jsonify({"error": "Incorrect password"}), 401
    
    access_token = create_access_token(identity={
        "id" : existing_user.id,
        "role" : existing_user.role
    })
    return jsonify({"message": "Login Successful", "access_token" : access_token}), 200

# User Logout  
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200

# User info - for storing token and login info in LocalStorage

@app.route("/userinfo", methods=["GET"])
@jwt_required()
def userinfo():
    current_user = get_jwt_identity()
    id = current_user["id"]
    user_exists = User.query.filter_by(id=id).first()
    if not user_exists:
        return jsonify({"error": "user does not exist"}), 404
    user = user_schema.dump(user_exists)
    return jsonify(user), 200

#New Section Route - C of CRUD
@app.route("/section",methods=["POST"])
@jwt_required()
def section():
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to create section"}), 401
    data = request.json
    name = data.get("name")
    description = data.get("description")
    current_date = datetime.now()
    create_id = cur_user["id"]

    section_exists = Section.query.filter_by(name=name).first()
    if section_exists:
        return jsonify({"error": "Section exists, trying to create a duplicate section"}), 406
    
    new_section = Section(name=name, description=description, create_date=current_date,create_id=create_id, update_date=current_date, update_id=create_id)
    try:
        db.session.add(new_section)
        db.session.commit()
        return jsonify({"message" : "New Section Created Successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error" : "Error Creating Section"}), 500

# Select all sections - R of CRUD
@app.route("/section", methods=["GET"])
@jwt_required()
def get_section():
   sections = Section.query.all()
   data = {"sections": sections_schema.dump(sections)}
   return jsonify(data)

# Select section by ID - Read
@app.route("/section/<int:section_id>", methods=["GET"])
@jwt_required()
def get_section_by_id(section_id):
   section = Section.query.filter_by(id=section_id).first()
   data = {"section": section_schema.dump(section)}
   return jsonify(data)


# Update section - U of CRUD
@app.route("/section/<int:section_id>", methods=["PUT"])
@jwt_required()
def upd_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"error": "Section not found"}), 404
    
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to update section"}), 401
    
    data = request.json
    name = data.get("name")
    description = data.get("description")
    update_date = datetime.now()
    update_id = cur_user["id"]

    section.name = name
    section.description = description
    section.update_date = update_date
    section.update_id = update_id

    try:
        db.session.commit()
        return jsonify({"message": "Section updated successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while update section: {str(e)}")
        return jsonify({"error": "Error while update Section"})


# Delete  section - D of CRUD
@app.route("/section/<int:section_id>", methods=["DELETE"])
@jwt_required()
def del_section(section_id):
    
    section = Section.query.get(section_id)

    if not section:
        return jsonify({"error": "Section not found"}), 404
        
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to delete section"}), 401
    
    try : 
        section = Section.query.get(section_id)
        db.session.delete(section)
        db.session.commit()
        return jsonify({"message":"Section deleted successfully"})
    except Exception as e :
        return jsonify({"error": "delete section not successful"}), 500
 

# New Book Route - C of CRUD
@app.route("/book/<int:section_id>", methods=["POST"])
@jwt_required()
def book(section_id):
        cur_user = get_jwt_identity()
        if cur_user["role"] != "librarian":
            return jsonify({"error": "Not authorized to create book"}), 401
        data = request.json
        name = data.get("name")
        content = data.get("content")
        authors = data.get("authors")
        book_path = data.get("book_path")
        section_id = section_id
        

        new_book = Book(name=name, content=content, authors=authors, book_path=book_path, section_id=section_id)
        try:
            db.session.add(new_book)
            db.session.commit()
            return jsonify({"message" : "New Book Created Successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error" : "Error Creating book"}), 500        
        
# Select all books in a section - R of CRUD
@app.route("/book/section/<int:id>", methods=["GET"])
@jwt_required()
def get_book_from_section(id):
   books = Book.query.filter_by(section_id=id)
   data = {"books": books_schema.dump(books)}
   print(jsonify(data))
   return jsonify(data)

# Select a particular book

@app.route("/book/<int:id>", methods=["GET"])
@jwt_required()
def get_book(id):
   book = Book.query.filter_by(id=id).first()
   data = {"book": book_schema.dump(book)}
   print(jsonify(data))
   return jsonify(data)

# Select all books that match wild card search - R of CRUD

#@app.route("/book/pattern/<string:pattern>", methods=["GET"])
#@jwt_required()
#def get_book_from_textpattern(pattern=''):
#   if not pattern:
#       books = Book.query.filter_by().all
#   else:
#       books = Book.query.filter(Book.name.like(f'%{pattern}%')|Book.authors.like(f'%{pattern}%')).all()
 
#   data = {"books": books_schema.dump(books)}
#   print(jsonify(data))
#   return jsonify(data)

# Select all books

@app.route("/book", methods=["GET"])
@jwt_required()
def get_all_books():
   book = Book.query.filter_by().all()
   data = {"books": books_schema.dump(book)}

   return jsonify(data)

# Update Book - U of CRUD
@app.route("/book/<int:book_id>", methods=["PUT"])
@jwt_required()
def upd_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to update book"}), 401
    
    data = request.json
    name = data.get("name")
    content = data.get("content")
    authors = data.get("authors")
    book_path = data.get("book_path")
    section_id = data.get("section_id")
    
    print(book)
    print(name, authors, book_path, section_id)
    
    book.name = name
    book.content = content
    book.authors = authors
    book.book_path = book_path
    book.section_id = section_id

    

    try:
        db.session.commit()
        return jsonify({"message": "Book updated successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while update Book: {str(e)}")
        return jsonify({"error": "Error while update Book"})



# Delete  section - D of CRUD
@app.route("/book/<int:book_id>", methods=["DELETE"])
@jwt_required()
def del_book(book_id):
    
    book = Book.query.get(book_id)
    cur_user = get_jwt_identity()
    if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to delete book"}), 401
    
    try : 
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message":"Book deleted successfully"})
    except Exception as e :
        return jsonify({"message":"Book was not deleted "})

# Transactions - Book Request

@app.route("/bookrequest/<int:user_id>/<int:book_id>", methods = ["POST"])
@jwt_required()
def bookrequest(user_id, book_id):
    cur_user = get_jwt_identity()
    if cur_user["role"] != "user":
        return jsonify({"error": "Not a user - can't request book"}), 401
    no_of_books = UserBook.query.filter_by(user_id=user_id).count()
    if ( no_of_books == 5 ):
        return jsonify({"error": "You have exceeded your quota of book issue and cannot request books"}), 429
    request_date =  datetime.now()
    status = "request"

    requestexists = UserBook.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
    if requestexists:
        return jsonify({"error": "Duplicate request"}), 406
    newreq = UserBook(user_id=user_id, book_id=book_id, request_date=request_date,issue_date=None, due_date=None, return_date=None, revoke_date=None, status=status)
    try:
        
        db.session.add(newreq)
        db.session.commit()
        return jsonify({"message" : "New book request created successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating new book request"}), 500

# Read Books Request by status ( request, approve, overdue, return, revoke - R of CRUD for Book Request table
@app.route("/bookrequest/status", methods=["GET"])
@jwt_required()
def get_bookrequest_by_status():
   cur_user = get_jwt_identity()
   if cur_user["role"] != "librarian":
        return jsonify({"error": "Not authorized to view book requests by status"}), 401
   bookreq = UserBook.query.filter((UserBook.status !="approve") & (UserBook.status !="return") & (UserBook.status !="reject")).all()
   data = {"bookrequest": user_books_schema.dump(bookreq)}
   return jsonify(data)

# Read Books Request by user ( request, approve, overdue, return, revoke - R of CRUD for Book Request table
@app.route("/bookrequest/user", methods=["GET"])
@jwt_required()
def get_bookrequest_by_user():
   cur_user = get_jwt_identity()
   if cur_user["role"] != "user":
        return jsonify({"error": "Only users can view their requests"}), 401
   status="return"
   user_id =  cur_user["id"]
   bookreq = UserBook.query.filter( (UserBook.user_id==user_id) & (UserBook.status !="return")).all()
   
   data = {"bookrequest": user_books_schema.dump(bookreq)}
   return jsonify(data)



# Update User book status (approve, reject, return, revoke, renew ) - U of CRUD
@app.route("/bookrequest/status/<int:id>", methods=["PUT"])
@jwt_required()
def upd_bookrequest_status(id):
    bookrequest = UserBook.query.filter_by(id=id).first()
    if not bookrequest:
        return jsonify({"error": "Book against user not found, can't fulfill update"}), 404
    
    cur_user = get_jwt_identity()
    data = request.json
    status = data.get("status")
    if cur_user["role"] == "librarian":
        print(status)
        if ( status == "return" or status == "renew" ):
            return jsonify({"error": "Status update request is not possible for librarian"}), 401
        if (status == "approve"):
            bookrequest.status = "approve"
            bookrequest.issue_date = datetime.now()
            bookrequest.due_date = datetime.now() + timedelta(days=7)
        if (status == "reject"):
            bookrequest.status = "reject"
        if (status == "revoke"):
            bookrequest.status = "revoke"
    if cur_user["role"] == "user":
        print(status)
        if ( status == "approve" or status == "reject" or status == "revoke"):
            return jsonify({"error": "Status update request is not possible for User"}), 401
        if (status == "return"):
            bookrequest.status = "return"
            bookrequest.return_date = datetime.now()
        if (status == "renew"):
            bookrequest.status = "renew"

    try:
        db.session.commit()
        return jsonify({"message": "Book request updated successfully"})
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred while update book request status: {str(e)}")
        return jsonify({"error": "Error while update book request status"})

if __name__ =="__main__":
    app.run(debug=True)