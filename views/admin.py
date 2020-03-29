import json
from flask import Blueprint, render_template, request, redirect, url_for,jsonify,logging,flash
from models.scrap_elem import ScrapElem
from models.scrap_data import Scrap
from models.user.decorators import requires_admin
from function.run_spider import run_spider


admin_blueprint = Blueprint('admin',__name__)


@admin_blueprint.route('/')
@requires_admin
def index():
    return render_template('admin/admin_index.html')


@admin_blueprint.route('/update', methods=['GET', 'POST'])
@requires_admin
def update_property():
    # Scrap.integrateData()
    try:
        Scrap.integrateData()
        flash('Update success', 'success')
    except:
        flash('Update fail', 'danger')
    return render_template('admin/admin_index.html')

# @admin_blueprint.route('/update/updating')
# def scraping_process():
#     scrap_elem = ScrapElem.all()
#     for elem in scrap_elem:
#         # try:
#         Scrap.scrap_one(elem.list_page_url, elem.source)
#         # except :
#         #     pass
#     # Scrap('tmb', 'ธนาคารทหารไทย', 'https://www.tmbbank.com/property/property/for-sale', '(02) 242-3244, (02) 242-3245, (02) 242-3246, (02) 242-3211', ['https://media.tmbbank.com/uploads/npa/product/gallery/large/315_180615060924_1.jpg','https://media.tmbbank.com/uploads/npa/product/gallery/large/315_180615060925_2.jpg'], ['https://media.tmbbank.com/uploads/npa/product/map/315_20180615180924.jpg'], 'บ้าน', 'B12284', '4,200,000', '0000-0-52.0', 0, 0, 52, 'ฉ.106719').save_to_mongo()
   
#     return redirect(url_for('admin.update_property',m='Success'))
    # try:
        
    # except :
    #     return redirect(url_for('admin.update_property',m='Fail'))

    # return render_template('admin/update_property.html',all_elem = ScrapElem.all())
    
    

@admin_blueprint.route('/setting', methods=['GET','POST'])
@requires_admin
def update_setting():
    if request.method == 'POST':
        list_page_url = request.form['list_page_url']
        source = request.form.get('source-select')
        print(list_page_url)
        print(source)
        scrap_elem = ScrapElem.find_by_source(source)
        scrap_elem.list_page_url = list_page_url
        scrap_elem.save_to_mongo()

   
    # ScrapElem('https://www.tmbbank.com/property/property/for-sale','tmb', 'ธนาคารทหารไทย',_id='011').save_to_mongo()
    return render_template('admin/update_setting.html', scrap_elem=ScrapElem ,all_elem=ScrapElem.all())



@admin_blueprint.route('/setting/scraping')
@requires_admin
def scraping_setting():

    return render_template('admin/scraping_setting.html',sources=ScrapElem.all())

@admin_blueprint.route('/setting/scraping/new', methods=['GET','POST'])
@requires_admin
def new_source():
    if request.method =='POST':
        _id = request.form['_id']
        source = request.form['source']
        source_name = request.form['source_name']
        url = request.form['url']
        base_url = request.form['base_url']
        item_page = request.form['item_page']
        next_page = request.form['next_page']
        img = request.form['img']
        gg_map = request.form['gg_map']
        price = request.form['price']
        asset_type = request.form['asset_type']
        asset_code = request.form['asset_code']
        area = request.form['area']
        deed_num = request.form['deed_num']
        address = request.form['address']
        contact = request.form['contact']
        more_detail = request.form['more_detail']

        try:
            ScrapElem(
                source = source,
                source_name = source_name,
                url = url,
                base_url = base_url, 
                item_page = item_page,
                next_page = next_page, 
                img = img,
                gg_map = gg_map,
                price = price, 
                asset_type = asset_type,
                asset_code = asset_code,
                area = area,
                deed_num = deed_num,
                address = address,
                contact = contact,
                more_detail = more_detail ,
                _id=_id
            ).save_to_mongo()
            flash('Create source success', 'success')
            return redirect(url_for('admin.scraping_setting'))
        except:
            flash('Create source fail', 'danger')



    return render_template('admin/new_source.html')


@admin_blueprint.route('/setting/scraping/<string:source_id>', methods=['GET','POST'])
@requires_admin
def edit_source(source_id):
    if request.method =='POST':
        source = request.form['source']
        source_name = request.form['source_name']
        url = request.form['url']
        base_url = request.form['base_url']
        item_page = request.form['item_page']
        next_page = request.form['next_page']
        img = request.form['img']
        gg_map = request.form['gg_map']
        price = request.form['price']
        asset_type = request.form['asset_type']
        asset_code = request.form['asset_code']
        area = request.form['area']
        deed_num = request.form['deed_num']
        address = request.form['address']
        contact = request.form['contact']
        more_detail = request.form['more_detail']

        source_data = ScrapElem.find_one_by('_id',source_id)
        
        source_data.source = source
        source_data.source_name = source_name
        source_data.url = url
        source_data.base_url = base_url
        source_data.item_page = item_page
        source_data.next_page = next_page
        source_data.img = img
        source_data.gg_map = gg_map
        source_data.price = price
        source_data.asset_type = asset_type
        source_data.asset_code = asset_code
        source_data.area = area
        source_data.deed_num = deed_num
        source_data.address = address
        source_data.contact = contact
        source_data.more_detail = more_detail
        try:
            source_data.save_to_mongo()
            flash('Edited', 'success')
        except:
            flash('Edit fail', 'danger')
        
        return redirect(url_for('admin.edit_source',source_id = source_id))


    return render_template('admin/edit_source.html',source_data=ScrapElem.find_one_by('_id',source_id))

@admin_blueprint.route('/setting/scraping/<string:source_id>/delete')
@requires_admin
def delete_source(source_id):
    target =  ScrapElem.find_one_by('_id',source_id)
    target.remove_from_mongo()
    flash(target.source_name +  " is deleted","success")
    return redirect(url_for('admin.scraping_setting'))

@admin_blueprint.route('/setting/scraping/runspider')
@requires_admin
def start_scraping():
    run = run_spider()
    flash(run,"warning")
    return redirect(url_for('admin.scraping_setting'))


