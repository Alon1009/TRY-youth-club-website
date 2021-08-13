from model import Base, Make_account, Create_workshop, Registered_users, Create_news

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail
from flask_mail import Message
from flask import session as login_session
engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

import os
from flask import Flask, jsonify, request, render_template, url_for, redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import random
import requests, json

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = 'static/images'
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


def add_new_workshop(workshop_name, details, pictures, max_registers):
    new_workshop = Create_workshop(workshop_name=workshop_name, details=details, pictures=pictures, max_registers=max_registers)
    session.add(new_workshop)
    session.commit()
    

def add_news(news_title, details, pictures):
    new_news = Create_news(news_title=news_title, details=details, pictures=pictures)
    session.add(new_news)
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

def get_workshop_by_id(id):
    workshop = session.query(
        Create_workshop).filter_by(
        id=id).first()
    return workshop
def get_news_by_id(id):
    news = session.query(
        Create_news).filter_by(
        id=id).first()
    return news

def delete_workshop(workshop_id):
    session.query(Create_workshop).filter_by(id=workshop_id).delete()
    session.commit()


def delete_new(new_id):
    session.query(Create_news).filter_by(id=new_id).delete()
    session.commit()


def delete_register(register_id):
    session.query(Registered_users).filter_by(id=register_id).delete()
    session.commit()


def delete_register_by_workshop(workshop_id):
    session.query(Registered_users).filter_by(workshop_id=workshop_id).delete()
    session.commit()


def delete_register_by_user(user_id):
    session.query(Registered_users).filter_by(user_id=user_id).delete()
    session.commit()


def get_all_users():
    users = session.query(Make_account).all()
    return users


def get_all_workshops():
    workshops = session.query(Create_workshop).all()
    return workshops


def get_all_news():
    workshops = session.query(Create_news).all()
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
    new_account = Make_account(first_name=first_name, last_name=last_name, email=the_email, admin=admin)
    new_account.hash_password(password)
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


@app.route('/home', methods=['GET', 'POST'])
def login():
    if login_session["login"] != True:
        login_session["login"] = False
    if request.method == 'POST':
        login_email = request.form['email']
        password = request.form['password']
        login_session["email"] = login_email
        if get_account(login_email) is None:
            return render_template('login.html', login_info=False)
        else:
            if get_account(login_session["email"]).verify_password(password):
                print("login successful")
                login_session["login"] = True
                login_session["isAdmin"] = get_account(login_session["email"]).admin
                return render_template('index.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"])
            else:
                print("login info incorrect")
                return render_template('login.html', login_info=False)
    else:
        return render_template('index.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"])


@app.route('/', methods=['GET'])
def home():
    login_session["email"] = ''
    login_session["login"] = False
    login_session["isAdmin"] = False
    return redirect('/home')


@app.route('/donate', methods=['GET'])
def donate():
    return render_template('donate.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"])


@app.route('/donatePointer', methods=['GET'])
def donatePointerToMEET():
    return render_template('donatePointer.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"])


@app.route('/login', methods=['GET', 'POST'])
def login_2():
    if request.method == 'POST':
        login_email = request.form['email']
        password = request.form['password']
        login_session["email"] = login_email
        if get_account(login_email) is None:
            return render_template('login.html', login_info=False)
        else:
            if get_account(login_session["email"]).verify_password(password):
                print("login successful")
                login_session["login"] = True
                login_session["isAdmin"] = get_account(login_session["email"]).admin
                return redirect('/home')
            else:
                print("login info incorrect")
                return render_template('login.html', login_info=False)
    else:

        return render_template('login.html', login_info=True)



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        get_email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        login_session["email"] = get_email
        if login_session["email"] == "" or password == "" or first_name == "" or last_name == "":
            return render_template('sign_up.html', empty=False)
        elif "@" not in login_session["email"] and "." not in login_session["email"]:
            return render_template('sign_up.html', emailError=False)
        else:
            if get_account(login_session["email"]) is None:
                msg = Message("Hello", recipients=[login_session["email"]])         
                msg.html = "<b>Hey!</b>\nYou have successfully signed up on our TRY website, by signing up you will be getting notifications on our latest news, upcoming events and workshops.\nWe are thrilled to share our amazing journey with you!\nFor more information you can reach out through this email: try.club2021@gmail.com"
                mail.send(msg)
                login_session["login"] = True
                login_session["isAdmin"] = False
                sign_up_database(get_email, first_name, last_name, password, login_session["isAdmin"])
                return redirect('/home')
            else:
                return render_template('sign_up.html', exists=False)
    else:
        return render_template('sign_up.html')


@app.route('/workshops', methods=['GET'])
def workshops():
    user_already_registered = False
    registers_dict = { }
    already_registered = { }
    workshops = get_all_workshops()
    registered = get_all_registered()
    for workshop in workshops:
        for register in registered:
            if workshop.id == register.workshop_id:
                if login_session["email"] != '':
                    if register.user_id == get_account(login_session["email"]).id:
                        user_already_registered = True
                if registers_dict.get(workshop.id) is None:
                    registers_dict[workshop.id] = 1
                else:
                    registers_dict[workshop.id] += 1
            if registers_dict.get(workshop.id) is None:
                registers_dict[workshop.id] = 0
        if registered == []:
            registers_dict[workshop.id] = 0
        already_registered[workshop.id] = user_already_registered
        user_already_registered = False
    return render_template('workshops.html', login=login_session["login"], email=login_session["email"], workshops=workshops, admin=login_session["isAdmin"], registers_dict=registers_dict, already_registered=already_registered)


@app.route('/news', methods=['GET'])
def news():
    news = get_all_news()
    return render_template('news.html', login=login_session["login"], email=login_session["email"], news=news, admin=login_session["isAdmin"])


@app.route('/ambassador', methods=['GET'])
def ambassador():
    return render_template('embasiders.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"])


@app.route('/admin_page_page', methods=['GET'])
def admin_page_1():
    users = get_all_users()
    workshops = get_all_workshops()
    registered = get_all_registered()
    news = get_all_news()
    if login_session["isAdmin"] == True:
        return render_template('admin.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"], users=users, workshops=workshops, registered=registered, news=news)
    else:
        return redirect('/home')


@app.route('/add_workshop', methods=['GET', 'POST'])
def add_workshop():
    if request.method == 'POST':
        workshop_name = request.form['workshop_name']
        workshop_details = request.form['workshop_details']
        max_registers = request.form['max_registers']
        f = request.files['file']
        filepath = ''
        if f.filename != '':
            f.save(secure_filename(f.filename))
            filepath = "static/images/" + f.filename 
            os.rename(f.filename, filepath)
        add_new_workshop(workshop_name, workshop_details, filepath, max_registers)
        users = get_all_users()
        workshops = get_all_workshops()
        return redirect('/admin_page_page')
    else:
        return render_template('add_workshop.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"])


@app.route('/add_news', methods=['GET', 'POST'])
def add_the_news():
    if request.method == 'POST':
        news_title = request.form['news_title']
        news_details = request.form['news_details']
        f = request.files['file']
        filepath = ''
        if f.filename != '':
            f.save(secure_filename(f.filename))
            filepath = "static/images/" + f.filename 
            os.rename(f.filename, filepath)
        news_pictures = filepath
        add_news(news_title, news_details, news_pictures)
        return redirect('/admin_page_page')
    else:
        return render_template('add_news.html', login=login_session["login"], email=login_session["email"], admin=login_session["isAdmin"])


@app.route('/register_to_a_workshop/<int:workshop_id>', methods=['GET', 'POST'])
def register_workshop(workshop_id):
    show = True
    overload = False
    workshops = get_all_workshops()
    registered = get_all_registered()
    registers_dict = {}
    for workshop in workshops:
        for register in registered:
            if workshop.id == register.workshop_id:
                if registers_dict.get(workshop.id) is None:
                    registers_dict[workshop.id] = 1
                else:
                    registers_dict[workshop.id] += 1
            if registers_dict.get(workshop.id) is None:
                registers_dict[workshop.id] = 0
        if registered == []:
            registers_dict[workshop.id] = 0
    if login_session["email"] != '':
        user_id = get_account(login_session["email"]).id
        registered_by_id = get_all_registered_by_id(workshop_id)
        for register in registered_by_id:
            if register.user_id == user_id:
                show = False
    if get_workshop_by_id(workshop_id).max_registers <= registers_dict.get(workshop_id):
        overload = True
    if login_session["login"] == True and show and overload == False:
        register_to_workshop(workshop_id, user_id)
        msg = Message("Hello", recipients=[login_session["email"]])
        msg.html = "You have successfully registered for our upcoming workshop!\nThe workshop will be held in our youth club in Nazareth (TRY youth club), from 17:00 - 20:00.\nFor more information you can reach out through this email: try.club2021@gmail.com\nPlease confirm your coming by simply replying to this message.\nThank you!"
        mail.send(msg)
    return redirect('/workshops')


@app.route('/log_out', methods=['GET'])
def log_out():
    login_session["login"] = False
    login_session["isAdmin"] = False
    login_session["email"] = ''
    return redirect('/home')


@app.route('/remove_user/<string:user_email>', methods=['GET'])
def remove_user_from_database(user_email):
    user_id = get_account(user_email).id
    delete_user(user_email)
    delete_register_by_user(user_id)
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
    workshop1 = get_workshop_by_id(workshop_id)
    if workshop1.pictures != '':
        os.remove(workshop1.pictures) 
    delete_workshop(workshop_id)
    delete_register_by_workshop(workshop_id)
    return redirect('/admin_page_page')


@app.route('/remove_news/<string:news_id>', methods=['GET'])
def delete_news_from_id(news_id):
    news1 = get_news_by_id(news_id)
    if news1.pictures != '':
        os.remove(news1.pictures) 
    delete_new(news_id)
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
