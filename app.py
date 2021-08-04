from model import Base, Make_account, Create_workshop, Registered_users

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail
from flask_mail import Message

engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
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

app.config['TESTING'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'naztry.club@gmail.com'
app.config['MAIL_PASSWORD'] = 'try.club(2021)'
app.config['MAIL_DEFAULT_SENDER'] = ('TRY', 'naztry.club@gmail.com')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_MAX_EMAILS'] = 1
app.config['MAIL_ASCII_ATTACHMENTS'] = False
# app.config['MAIL_SUPPRESS_SEND'] = False
# app.config['MAIL_DEBUG'] = True
mail = Mail(app)

login = False
isAdmin = False
email = ""


def add_new_workshop(workshop_name, details, pictures):
    new_workshop = Create_workshop(workshop_name=workshop_name, details=details, pictures=pictures)
    session.add(new_workshop)
    session.commit()
    

def register_to_workshop(workshop_id, user_id):
    new_regsiter = Registered_users(workshop_id, user_id)
    session.add(new_regsiter)
    session.commit()


def get_workshop(name):
    workshop = session.query(
        Create_workshop).filter_by(
        workshop_name=name).first()
    return workshop


def delete_workshop(workshop_id):
    session.query(Create_workshop).filter_by(id=workshop_id).delete()
    session.commit()


def get_all_users():
    users = session.query(Make_account).all()
    return users


def get_all_workshops():
    workshops = session.query(Create_workshop).all()
    return workshops


def get_account(their_email):
    account = session.query(
        Make_account).filter_by(
        email=their_email).first()
    return account


def sign_up_database(the_email, first_name, last_name, password, admin):
    new_account = Make_account(first_name=first_name, last_name=last_name, email=the_email, password=password, admin=admin)
    session.add(new_account)
    session.commit()


def delete_user(user_email):
    session.query(Make_account).filter_by(email=user_email).delete()
    session.commit()

def update_admin(user, isActuallyAdmin):
    user.admin = isActuallyAdmin
    session.commit()


@app.route('/', methods=['GET'])
def home():
    global email
    global login
    login = False
    isAdmin = False
    return render_template('index.html', login=login, email=email, admin=isAdmin)


@app.route('/home', methods=['GET', 'POST'])
def login():
    global email
    global login
    isAdmin = False
    if login != True:
        login = False
    if request.method == 'POST':
        login_email = request.form['email']
        password = request.form['password']
        email = login_email
        if get_account(login_email) is None:
            return render_template('login.html', login=login, email=email, login_info=False)
        else:
            isAdmin = get_account(email).admin
            if password == get_account(login_email).password:
                print("login successful")
                login = True
                return render_template('index.html', login=login, email=email, admin=isAdmin)
            else:
                print("login info incorrect")
                return render_template('login.html', login=login, login_info=False)
    else:
        return render_template('index.html', login=login, email=email, admin=isAdmin)


@app.route('/login', methods=['GET', 'POST'])
def login_2():
    global email
    global login
    if request.method == 'POST':
        login_email = request.form['email']
        password = request.form['password']
        email = login_email
        if get_account(login_email) is None:
            return render_template('login.html', login=login, email=email, login_info=False)
        else:
            isAdmin = get_account(email).admin
            if password == get_account(login_email).password:
                print("login successful")
                login = True
                return render_template('index.html', login=login, email=email, admin=isAdmin)
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
        msg = Message("Hello", recipients=[email])         
        msg.html = "<b>Hi there user \nWelcome!</b>"
        mail.send(msg)
        if email == "" or password == "" or first_name == "" or last_name == "":
            return render_template('sign_up.html', login=login, email=email, empty=False)
        elif "@" not in email and "." not in email:
            return render_template('sign_up.html', login=login, email=email, emailError=False)
        else:
            if get_account(email) is None:
                login = True
                adminValue = False
                sign_up_database(get_email, first_name, last_name, password, adminValue)
                return render_template('index.html', login=login, email=email, login_info=True, admin=adminValue)
            else:
                return render_template('sign_up.html', login=login, email=email, exists=False)
    else:
        return render_template('sign_up.html')


@app.route('/news', methods=['GET', 'POST'])
def news():
    global email
    global login
    workshops = get_all_workshops()
    if request.method == 'POST':
        return render_template('news.html', login=login, email=email, workshops=workshops)
    else:
        return render_template('news.html', login=login, email=email, workshops=workshops)

@app.route('/add_workshop', methods=['GET', 'POST'])
def add_workshop():
    global email
    global login
    if request.method == 'POST':
        workshop_name = request.form['workshop_name']
        workshop_details = request.form['workshop_details']
        workshop_pictures = request.form['workshop_pictures']
        add_new_workshop(workshop_name, workshop_details, workshop_pictures)
        users = get_all_users()
        workshops = get_all_workshops()
        return render_template('admin.html', login=login, email=email, users=users, workshops=workshops)
    else:
        return render_template('add_workshop.html', login=login, email=email)


@app.route('/register_to_workshop/<string:workshop_name>', methods=['GET', 'POST'])
def register_workshop(workshop_name):
    global email
    global login
    if login == True:
        msg = Message("Hello", recipients=[email])
        msg.html = "<b>Hi there user \nWelcome!</b>"
        mail.send(msg)
    workshop_id = get_workshop("test").id
    user_id = get_account(email).id
    register_to_workshop(workshop_id, user_id)
    return render_template('news.html', login=login, email=email)


@app.route('/log_out', methods=['GET', 'POST'])
def log_out():
    global email
    global login
    login = False
    if request.method == 'POST':
        return render_template('index.html', login=login, email=email)
    else:
        return render_template('index.html', login=login, email=email)


@app.route('/admin_page_page', methods=['GET'])
def admin_page_1():
    global email
    global login
    global admin
    users = get_all_users()
    workshops = get_all_workshops()
    return render_template('admin.html', login=login, email=email, users=users, workshops=workshops)


@app.route('/remove_user/<string:user_email>', methods=['GET'])
def remove_user_from_database(user_email):
    global email
    global login
    delete_user(user_email)
    users = get_all_users()
    workshops = get_all_workshops()
    return render_template('admin.html', login=login, email=email, users=users, workshops=workshops)

@app.route('/make_user_admin/<string:user_email>', methods=['GET'])
def make_user_admin(user_email):
    global email
    global login
    update_admin(get_account(user_email), True)
    users = get_all_users()
    workshops = get_all_workshops()
    return render_template('admin.html', login=login, email=email, users=users, workshops=workshops)


@app.route('/demote_user_admin/<string:user_email>', methods=['GET'])
def demote_user_admin(user_email):
    global email
    global login
    update_admin(get_account(user_email), False)
    users = get_all_users()
    workshops = get_all_workshops()
    return render_template('admin.html', login=login, email=email, users=users, workshops=workshops)


@app.route('/remove_workshop/<string:workshop_id>', methods=['GET'])
def delete_workshop_with_id(workshop_id):
    global email
    global login
    delete_workshop(workshop_id)
    users = get_all_users()
    workshops = get_all_workshops()
    return render_template('admin.html', login=login, email=email, users=users, workshops=workshops)


if __name__ == "__main__":  # Makes sure this is t
    app.run(
        host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
        port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
        debug=True)