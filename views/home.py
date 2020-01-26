from flask import Blueprint, request, session, url_for, render_template, redirect




home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def index():
    return render_template('home.html')
    