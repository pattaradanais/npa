from flask import Blueprint, request, session, url_for, render_template, redirect
# from models.user import User, UserErrors
from models.scrap_data import Scrap
from flask_paginate import Pagination, get_page_parameter

property_blueprint = Blueprint('property',__name__)

@property_blueprint.route('/',methods=['GET'])
def index():
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    data = Scrap.all()
    print(len(data))
    pagination = Pagination(css_framework='bootstrap4' ,page=page, per_page=12, total=len(data), search=search, record_name='data')
    return render_template('property.html',data=data, pagination=pagination)


@property_blueprint.route('/<string:_id>',methods=['GET'])
def property_item(_id):
    item = Scrap.find_one_by("_id",_id)
    return render_template('property_item.html', item=item)