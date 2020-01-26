import os
from flask import Flask, render_template,session
# from views.alerts import alert_blueprint
# from views.stores import store_blueprint
from views.users import user_blueprint
from views.admin import admin_blueprint
from views.home import home_blueprint
from models.user.user import User
from common.database import Database

app = Flask(__name__)
app.config.from_object('.config')
app.secret_key = os.urandom(64)

# app.config.update(
#     ADMIN=os.environ.get('ADMIN')
  
# )

@app.before_first_request
def init_db():
    Database.initialize()

app.register_blueprint(home_blueprint, url_prefix="/")
# app.register_blueprint(alert_blueprint, url_prefix="/alerts")
# app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(admin_blueprint, url_prefix="/admin")

@app.context_processor
def user_data():
    try:
        return dict(user =User.find_by_email(session['email']))
    except :
        return dict(user = None)
    

# @app.route('/')
# def base():
#     try:
#         user = User.find_by_email(session['email'])
#     except:
#         user = None
#     return render_template('base.html', user=user)

if __name__ == "__main__":
    app.run()
