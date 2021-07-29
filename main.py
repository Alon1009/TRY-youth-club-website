from model import Base, Make_account

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import Flask, jsonify, request, render_template, url_for, redirect
import random
import requests, json

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)

login = False
email = None


def get_account(their_email):
    account = session.query(
        Make_account).filter_by(
        email=their_email).first()
    return account




def sign_up_database(email, first_name, last_name, password):
    new_account = Make_account(first_name=first_name, last_name=last_name, email=email,password=password)
    session.add(new_account)
    session.commit()




@app.route('/', methods=['GET', 'POST'])
def login():
    global email
    global login
    if login != True:
        login = False
    if request.method == 'POST':
        login_email = request.form['email']
        password = request.form['password']
        email = login_email
        if get_account(login_email) is None:
            return render_template('login.html', login=login, email=email, login_info=False)
        else:
            if password == get_account(login_email).password:
                print("login successful")
                login = True
                return render_template('index.html', login=login, email=email)
            else:
                print("login info incorrect")
                return render_template('login.html', login=login, login_info=False)
    else:
        return render_template('index.html', login=login, email=email)


@app.route('/login', methods=['GET', 'POST'])
def login_2():
    global email
    global login
    if request.method == 'POST':
        login_email = request.form['email']
        password = request.form['password']
        email = login_email
        if get_account(login_email) is None:
            return render_template('login.html', login=login, wmail=email, login_info=False)
        else:
            if password == get_account(login_email).password:
                print("login successful")
                login = True
                return render_template('index.html', login=login, email=email)
            else:
                print("login info incorrect")
                return render_template('login.html', login=login, login_info=False)
    else:

        return render_template('login.html', login=login, login_info=True)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    global email
    global login
    if request.method == 'POST':
        get_email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = get_email
        if email == "" or password == "" or first_name == "" or last_name == "":
          return render_template('sign_up.html', login=login, email=email, empty=False)
        elif "@" not in email and "." not in email:
          return render_template('sign_up.html', login=login, email=email, emailError=False) 
        else:
          if get_account(email) is None:
            login = True
            sign_up_database(get_email, first_name, last_name, password)
            return render_template('index.html', login=login, email=email, login_info=True)
          else:
            return render_template('sign_up.html', login=login, email=email, exists=False)
    else:
        return render_template('sign_up.html')


@app.route('/donate', methods=['GET','POST'])
def donate():
    global email
    global login
    if request.method == 'POST':
        return render_template('thankyou.html', login=login, email=email)
    else:
        return render_template('donate.html', login=login, email=email)


@app.route('/news', methods=['GET','POST'])
def news():
    global email
    global login
    if request.method == 'POST':
        return render_template('newsWorkShop.html', login=login, email=email)
    else:
        return render_template('newsWorkShop.html', login=login, email=email)


@app.route('/log_out', methods=['GET','POST'])
def log_out():
    global email
    global login
    login = False
    if request.method == 'POST':
        return render_template('index.html', login=login, email=email)
    else:
        return render_template('index.html', login=login, email=email)



@app.route('/about', methods=['GET','POST'])
def aboutUs():
    global email
    global login
    if request.method == 'POST':
        return render_template('abo.html', login=login, email=email)
    else:
        return render_template('abo.html', login=login, email=email)


@app.route('/contact', methods=['GET','POST'])
def contactUs():
    global email
    global login
    if request.method == 'POST':
        return render_template('contact.html', login=login, email=email)
    else:
        return render_template('contact.html', login=login, email=email)


if __name__ == "__main__":  # Makes sure this is t
    app.run(
        host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
        port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
        debug=True)
