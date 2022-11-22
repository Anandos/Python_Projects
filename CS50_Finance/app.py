# I implemented all wrapped functions, except login and logout in app.py

import os
import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():                                              # Portfolio
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    data = db.execute(f"SELECT * FROM shares WHERE id={user_id};")
    total_shares_value = 0
    print(data)
    i = 0
    for row in data:
        lookup_symbol = lookup(row['symbol'])
        data[i]['name'] = lookup_symbol['name']
        data[i]['price'] = lookup_symbol['price']
        data[i]['total'] = round(data[i]['price'] * data[i]['shares'], 2)
        total_shares_value += data[i]['total']
        i += 1
        print(lookup_symbol, row)

    user_cash = db.execute(f"SELECT cash FROM users WHERE id={user_id};")[0]['cash']
    print(user_cash)

    return render_template("portfolio.html", cash=user_cash, data=data, total_shares_value=total_shares_value)

    return apology("No Shares owned yet")  # It's better to show an empty portfolio table rather than an error page here imo


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():                                              # Sell
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":
        # get list of symbols and shares for each, put into table
        # get symbol
        data = db.execute(f"SELECT * FROM shares WHERE id={user_id};")
        print("data json for user symbol list:", data)
        return render_template("sell.html", data=data)

    elif request.method == "POST":
        # get user input
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))

        # get symbol data from API
        data = lookup(symbol)

        # Calculate cost of shares
        cost = shares * data['price']
        # Append cost of shares into Users table
        user_cash = db.execute(f"SELECT cash FROM users WHERE id={user_id};")[0]['cash']
        print(type(user_cash), user_cash)
        user_cash = user_cash + cost
        db.execute(f"UPDATE users SET cash={user_cash} WHERE id={user_id};")

        # Update shares number in Shares table
        user_shares = db.execute(f"SELECT shares FROM shares WHERE id={user_id} AND symbol='{symbol}';")[0]['shares']
        print(user_shares)
        user_shares = user_shares - shares
        db.execute(f"UPDATE shares SET shares={user_shares} WHERE id={user_id} AND symbol='{symbol}';")

        # Then create new row in Ledger table for transaction
        date_seconds = str(datetime.datetime.now().replace(microsecond=0))
        db.execute(
            f"INSERT INTO ledger (id, symbol, shares, price, date) VALUES ({user_id}, '{symbol}', -{shares}, {cost}, '{date_seconds}');")

        return render_template("sell.html", symbol=symbol, shares=shares, price=usd(data['price']))

    return apology("Unknown Sell Error")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():                                              # Buy
    """Buy shares of stock"""

    user_id = session["user_id"]  # ger user id no.

    if request.method == "GET":
        return render_template("buy.html")  # Get Buy Form

    elif request.method == "POST":
        # Get user input
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        print("type ", type(shares))
        if type(shares) != int:  # Error check user's share number input
            return apology("Share Number is not a number")
        if shares < 1:
            return apology("Share Number Error")

        iex_json = lookup(symbol)  # get symbol price from IEX
        print("iex_symbol print: ", type(iex_json))
        if type(iex_json) == None:
            return apology("Invalid Symbol")

        cash = db.execute(f"SELECT cash FROM users WHERE id={user_id}")[0]['cash']  # get cash holding of user
        cost = float(iex_json["price"]) * int(shares)  # Total cost of shares of symbol
        print("POST", iex_json, cost, shares)

        if cash >= cost:
            # check if user has bought share before in shares table
            if db.execute(f"SELECT * FROM shares WHERE id={user_id} AND symbol='{symbol}';"):
                # UPDATE shares for symbol for users
                current_shares = db.execute(f"SELECT shares FROM shares WHERE id={user_id} AND symbol='{symbol}';")[0]
                print("current shares, shares", current_shares, shares)
                update_shares = int(current_shares['shares']) + int(shares)
                db.execute(f"UPDATE shares SET shares={update_shares} WHERE id={user_id} AND symbol='{symbol}';")
            else:  # Else make new row for share in shares table
                db.execute(f"INSERT INTO shares (id, symbol, shares) VALUES ({user_id}, '{symbol}', {shares});")

            # Then create new row in ledger table for transaction
            date_seconds = str(datetime.datetime.now().replace(microsecond=0))
            db.execute(
                f"INSERT INTO ledger (id, symbol, shares, price, date) VALUES ({user_id}, '{symbol}', {shares}, {iex_json['price']}, '{date_seconds}');")

            # deduct cost of shares from users table and Update user cash total
            update_cash = cash - cost
            db.execute(f"UPDATE users SET cash={update_cash} WHERE id={user_id};")

            return render_template("buy.html", bought=f"Bought {shares} shares of {symbol} at {usd(iex_json['price'])} each!")

        else:
            return apology("Not enough cash")

    return apology("Buy Error")


@app.route("/history")
@login_required
def history():                                              # History
    """Show history of transactions"""
    user_id = session["user_id"]
    ledger = db.execute(f"SELECT * FROM ledger WHERE id={user_id};")
    print(ledger)
    # if ledger:
    return render_template("history.html", ledger=ledger)

    return apology("History Error")


@app.route("/login", methods=["GET", "POST"])  # LOGIN Complete
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username #
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))  # Get username and password for user

        # Ensure username exists and password is correct #
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")  # LOGOUT Complete
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():                                              # Quote
    """Get stock quote."""
    if request.method == "GET":
        json = lookup("HBIO")

        return render_template("quote.html", json=json)

    if request.method == "POST":
        symbol = request.form.get("symbol")

        if symbol:
            json = lookup(symbol)

            if json != None:
                json['price'] = usd(json['price'])
                return render_template("quote.html", json=json)
            else:
                return apology(f"Invalid Symbol\n {symbol}")

    return apology("Unknown Symbol Error")


@app.route("/register", methods=["GET", "POST"])
def register():                                              # Register
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = request.form.get('confirmation')

        if username == "" or password == "":
            return apology("Username or password is empty")

        if password != password_check:
            print("passwords don't match")
            return apology("Passwords do not match")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 0:
            print("User already exists")
            return apology("Username already exists")

        hashed_password = generate_password_hash(password)

        print(f"INSERT INTO users (username, hash) VALUES ({username}, {hashed_password});")
        db.execute(f"INSERT INTO users (username, hash) VALUES ('{username}', '{hashed_password}');")
        print("fin")
        return render_template("register.html", success=f"Successfully registered {username}")

    return apology("Unknown Register Error")


# CREATE TABLE shares (id INTEGER, symbol TEXT, shares INTEGER);
# CREATE TABLE ledger (id INTEGER, symbol TEXT, shares INTEGER, price REAL, date TEXT);
# Primary Key should be unique entries, so 'id' in 'shares' and 'ledger' tables are not PK
