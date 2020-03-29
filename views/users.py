from flask import Blueprint, request, session, url_for, render_template, redirect
# from models.user import User, UserErrors
from models.user.user import User
import models.user.errors as UserErrors



user_blueprint = Blueprint('users', __name__)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    session.permanent = True
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('home.index'))
        except UserErrors.UserError as e:
            return render_template("users/login.html", message = e.message) 
    try:
        if  User.find_by_email(session['email']):
            return redirect(url_for('home.index'))
    except:
        pass


    return render_template("users/login.html")  # Send the user an error if their login was invalid

@user_blueprint.route('/logout')
def logout():
    session['email'] = None
    return redirect(url_for('.login_user'))


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        try:
            if User.register_user(name, lastname, email, password):
                session['email'] = email
                return redirect(url_for('home.index'))
        except UserErrors.UserError as e:
            return e.message
    
    try:
        if  User.find_by_email(session['email']):
            return redirect(url_for('home.index'))
    except:
        pass


    return render_template("users/register.html")  # Send the user an error if their login was invalid


@user_blueprint.route('/profile/<string:user_id>', methods={'GET', 'POST'})
def update_profile(user_id):
    if request.method == "POST":
        name = request.form['name']
        lastname = request.form['lastname']
        province = request.form['province']
        district = request.form['district']
        sub_district = request.form['sub_district']
        salary = request.form['salary']

        user = User.find_by_email(session['email'])
        user.name = name
        user.lastname = lastname
        user.province = province
        user.district = district
        user.sub_district = sub_district
        user.salary = salary

        user.save_to_mongo()

        return redirect(url_for('home.index'))


    return render_template('users/profile.html', user=User.find_by_email(session['email']))
