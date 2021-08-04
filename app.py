from model import Base, Make_account, Create_workshop, Registered_users

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail
from flask_mail import Message

engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import Flask, jsonify, request, render_template, url_for, redirect, flash
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
app.config['MAIL_USERNAME'] = 'try.club2021@gmail.com'
app.config['MAIL_PASSWORD'] = 'TryClub2021'
app.config['MAIL_DEFAULT_SENDER'] = ('TRY', 'try.club2021@gmail.com')
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
    new_regsiter = Registered_users(workshop_id=workshop_id, user_id=user_id)
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


def delete_register(register_id):
    session.query(Registered_users).filter_by(id=register_id).delete()
    session.commit()


def get_all_users():
    users = session.query(Make_account).all()
    return users


def get_all_workshops():
    workshops = session.query(Create_workshop).all()
    return workshops


def get_all_registered():
    registered = session.query(Registered_users).all()
    return registered

def get_all_registered_by_id(workshop_id):
    registered = session.query(
        Registered_users).filter_by(
        workshop_id=workshop_id).all()
    return registered



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


def update_workshop_1(workshop, workshop_name, details, pictures):
    workshop.workshop_name = workshop_name
    workshop.details = details
    workshop.pictures = pictures
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
    global isAdmin
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
    global isAdmin
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
    global isAdmin
    if request.method == 'POST':
        get_email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = get_email
        msg = Message("Hello", recipients=[email])         
        msg.html = "<b>Hey!</b>\nYou have successfully signed up on our TRY website, by signing up you will be getting notifications on our latest news, upcoming events and workshops.\nWe are thrilled to share our amazing journey with you!\nFor more information you can reach out through this email: try.club2021@gmail.com"
        mail.send(msg)
        if email == "" or password == "" or first_name == "" or last_name == "":
            return render_template('sign_up.html', login=login, email=email, empty=False)
        elif "@" not in email and "." not in email:
            return render_template('sign_up.html', login=login, email=email, emailError=False)
        else:
            if get_account(email) is None:
                login = True
                adminValue = False
                isAdmin = adminValue
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
    global isAdmin
    user = ''
    workshops = get_all_workshops()
    registered = get_all_registered()
    if email == '':
        user = ""
    else:
        user = get_account(email)
    if request.method == 'POST':
        return render_template('news.html', login=login, email=email, workshops=workshops, admin=isAdmin)
    else:
        return render_template('news.html', login=login, email=email, workshops=workshops, admin=isAdmin)

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


@app.route('/register_to_a_workshop/<int:workshop_id>', methods=['GET', 'POST'])
def register_workshop(workshop_id):
    global email
    global login
    show = True
    workshops = get_all_workshops()
    print("emailllll", email)
    if email != '':
        user_id = get_account(email).id
        registered = get_all_registered_by_id(workshop_id)
        for register in registered:
            if register.user_id == user_id:
                show = False
    if login == True and show:
        msg = Message("Hello", recipients=[email])
        msg.html = "You have successfully registered for our upcoming workshop!\nThe workshop will be held in our youth club in Nazareth (TRY youth club), from 17:00 - 20:00.\nFor more information you can reach out through this email: try.club2021@gmail.com\nPlease confirm your coming by simply replying to this message.\nThank you!"
        mail.send(msg)
        user_id = get_account(email).id
        register_to_workshop(workshop_id, user_id)
    return redirect('/news')


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
    global isAdmin
    users = get_all_users()
    workshops = get_all_workshops()
    registered = get_all_registered()
    if isAdmin == True:
        return render_template('admin.html', login=login, email=email, users=users, workshops=workshops, admin=isAdmin, registered=registered)
    else:
        return render_template('index.html', login=login, email=email, admin=isAdmin)


@app.route('/remove_user/<string:user_email>', methods=['GET'])
def remove_user_from_database(user_email):
    delete_user(user_email)
    return redirect('/admin_page_page')


@app.route('/make_user_admin/<string:user_email>', methods=['GET'])
def make_user_admin(user_email):
    update_admin(get_account(user_email), True)
    return redirect('/admin_page_page')


@app.route('/demote_user_admin/<string:user_email>', methods=['GET'])
def demote_user_admin(user_email):
    update_admin(get_account(user_email), False)
    return redirect('/admin_page_page')


@app.route('/remove_workshop/<string:workshop_id>', methods=['GET'])
def delete_workshop_with_id(workshop_id):
    delete_workshop(workshop_id)
    return redirect('/admin_page_page')


@app.route('/remove_register/<string:register_id>', methods=['GET'])
def delete_register_with_id(register_id):
    delete_register(register_id) 
    return redirect('/admin_page_page')


if __name__ == "__main__":  # Makes sure this is t
    app.run(
        host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
        port=random.randint(2000, 9000),  # Randomly select the port the machine hosts on.
        debug=True)
