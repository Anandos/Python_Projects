from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Connect SQLAlchemy to book database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_book_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)

# Create Database at start of project #
# db = sqlite3.connect("book_database.db")
# cursor = db.cursor()
# cursor.execute(
#     "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, "\
#     "title varchar(250) NOT NULL UNIQUE, "\
#     "author varchar(250) NOT NULL, "\
#     "rating FLOAT NOT NULL)"
#     )
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


# __________________________________________________________________________
# Render Flask website, and allows user to access/modify library database

@app.route('/')
def home():
    # Get list of all books and render on home page
    all_books = Book.query.all()
    return render_template("index.html", book_list= all_books)


@app.route("/add", methods= ["POST", "GET"])
def add():
    # Create new Book object from user's book input, add to database
    if request.method == "POST":
        # Convert form information into Book object
        new_book = Book(
            title= request.form['title'], 
            author= request.form['author'], 
            rating= float(request.form['rating'])
            )
        print(new_book)

        # Insert created Book object into SQLite database
        try:
            with app.app_context():
                db.create_all()
                db.session.add(new_book)
                db.session.commit()
        except:
            print("Error occured when writing book to database")

        return redirect(url_for("home"))

    # Present Book Adding Form
    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods= ["POST", "GET"])
def edit(book_id):
    # Get book from database, try to edit rating on database
    print("book id: ", book_id)
    book_to_edit = Book.query.get(book_id)

    if request.method == "POST":
        # Try to Edit book rating in database
        rating_edit = request.form['rating']
        print(rating_edit)

        try:
            with app.app_context():
                book_to_edit.rating = rating_edit
                db.session.merge(book_to_edit)
                db.session.commit()

        except:
            # If Error
            msg = "could not edit database"
            return render_template("error.html", msg= msg)

        return redirect(url_for("home"))
    
    # Present Rating Edit form
    return render_template("edit.html", book= book_to_edit)


@app.route("/delete/<int:book_id>", methods= ["POST", "GET"])
def delete(book_id):
    # Get book on database, try to delete book from database
    book_to_delete = Book.query.get(book_id)
    print(book_to_delete)

    try:
        with app.app_context():
            db.create_all()
            db.session.delete(book_to_delete)
            db.session.commit()
    except:
        # If Error
        msg = "Could not delete book"
        return render_template("error.html", msg= msg)
    
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

