import json
from flask import Blueprint, render_template, request, redirect, url_for,jsonify,logging
from models.scrap_elem import ScrapElem
from models.scrap_data import Scrap

from models.user.decorators import requires_admin

admin_blueprint = Blueprint('admin',__name__)


@admin_blueprint.route('/')
@requires_admin
def index():
    return render_template('admin/admin_index.html')


@admin_blueprint.route('/update', methods=['GET', 'POST'])
@requires_admin
def update_property():
    
    return render_template('admin/update_property.html',all_elem = ScrapElem.all())

@admin_blueprint.route('/update/updating')
def scraping_process():
    scrap_elem = ScrapElem.all()
    for elem in scrap_elem:
        # try:
        Scrap.scrap_one(elem.list_page_url, elem.source)
        # except :
        #     pass
    # Scrap('tmb', 'ธนาคารทหารไทย', 'https://www.tmbbank.com/property/property/for-sale', '(02) 242-3244, (02) 242-3245, (02) 242-3246, (02) 242-3211', ['https://media.tmbbank.com/uploads/npa/product/gallery/large/315_180615060924_1.jpg','https://media.tmbbank.com/uploads/npa/product/gallery/large/315_180615060925_2.jpg'], ['https://media.tmbbank.com/uploads/npa/product/map/315_20180615180924.jpg'], 'บ้าน', 'B12284', '4,200,000', '0000-0-52.0', 0, 0, 52, 'ฉ.106719').save_to_mongo()
   
    return redirect(url_for('admin.update_property',m='Success'))
    # try:
        
    # except :
    #     return redirect(url_for('admin.update_property',m='Fail'))

    # return render_template('admin/update_property.html',all_elem = ScrapElem.all())
    
    

@admin_blueprint.route('/setting', methods=['GET','POST'])
@requires_admin
def update_setting():
    if request.method == 'post':
        list_page_url = request.form['list_page_url']
        source = request.form.get('source-select')
        print(list_page_url)
        print(source)
        scrap_elem = ScrapElem.find_by_source(source)
        scrap_elem.list_page_url = list_page_url
        scrap_elem.save_to_mongo()

   
    # ScrapElem('https://www.tmbbank.com/property/property/for-sale','tmb', 'ธนาคารทหารไทย',_id='011').save_to_mongo()
    return render_template('admin/update_setting.html', scrap_elem=ScrapElem ,all_elem=ScrapElem.all())


@admin_blueprint.route('/setting/<string:source>', methods=['GET'])
@requires_admin
def query_source(source):
    query_data =  ScrapElem.find_by_source(source)

    return jsonify(query_data)