from flask import Blueprint, request, session, url_for, render_template, redirect
# from models.user import User, UserErrors
from models.scrap_data import Scrap
from models.scrap_elem import ScrapElem
from flask_paginate import Pagination, get_page_parameter
from bson.json_util import dumps,loads
import requests

property_blueprint = Blueprint('property',__name__)

@property_blueprint.route('/',methods=['GET', 'POST'])
def index():
    # api = 'https://npa-project.herokuapp.com/api/properties?page='
    # api = 'http://127.0.0.1:5000/api/properties?page='
    page = request.args.get('page') 

    if not page:
        page = '1'

    province = request.args.get('province',default='')
    district = request.args.get('district',default='')
    sub_district = request.args.get('sub_district',default='')
    asset_type = request.args.get('asset_type',default='')

    prov_arg = ''
    dist_arg = ''
    sub_dist_arg = ''
    type_arg = ''

    if request.method == 'POST':
        province = request.form.get('province')
        district = request.form.get('district')
        sub_district = request.form.get('sub_district')
        asset_type = request.form.get('asset_type')
        print(province)
        
        # page = '1'
        return redirect(url_for('property.index',province=province, district=district, sub_district=sub_district, asset_type=asset_type))

        # print(prov_arg,dist_arg,sub_dist_arg,type_arg)

        # print(str(province) + ' ' + str(district) + ' ' + str(sub_district) + ' ' + str(asset_type))
       
    if province:
        prov_arg = f'&province={province}' 
    if district:
        dist_arg = f'&district={district}'
    if sub_district:
        sub_dist_arg = f'&sub_district={sub_district}'
    if asset_type:
        type_arg = f'&asset_type={asset_type}'


    get_page_api =  requests.get(api + str(page) + str(prov_arg) + str(dist_arg) + str(sub_dist_arg) + str(type_arg))
    page_data = loads(get_page_api.text)
    search_args = f'{prov_arg}{dist_arg}{sub_dist_arg}{type_arg}'
    pagination = Pagination(page=int(page), total=page_data['total'], css_framework='bootstrap4',  record_name='properties',inner_window=5,search=True,found=page_data['count'],per_page=12, href="?page={0}"+search_args)
    return render_template('property.html',
                           data=page_data['result'],
                           pagination=pagination,
                           total=page_data['total'],
                           count=page_data['count']
                           )


@property_blueprint.route('/<string:_id>',methods=['GET'])
def property_item(_id):
    item = Scrap.find_one_by("_id",_id)
    source = ScrapElem.find_one_by("source",item.source)
    return render_template('property_item.html', item=item, source=source)
   