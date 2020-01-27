from flask import Blueprint, request, session, url_for, render_template, redirect
# from models.user import User, UserErrors
from models.scrap_data import Scrap

property_blueprint = Blueprint('property',__name__)

@property_blueprint.route('/',methods=['GET'])
def index():
    data = Scrap.all()
    return render_template('property',data=data)


@property_blueprint.route('/<string:_id>',methods=['GET'])
def property_item(_id):
    item = Scrap.find_one_by("_id",_id)
    return render_template('property_item', item=item)