import pymongo
from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
import json
import requests
from bson.json_util import dumps,loads
from flask_paginate import Pagination
from common.database import Database


# URI = "mongodb://npaDB:npaadmin@cluster0-shard-00-00-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-01-ipibu.gcp.mongodb.net:27017,cluster0-shard-00-02-ipibu.gcp.mongodb.net:27017/npaWebAppDB?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(Database.URI)
db = client.get_default_database()
# db = Database.DATABASE
col = db['properties']


class Property(Resource):
    def get(self):
        
   
        total = col.count()
        page = int(request.args['page'])
        limit = 12
        offset = (page - 1)*limit
        

        province = request.args.get('province') 
        district = request.args.get('district')
        sub_district = request.args.get('sub_district')
        asset_type = request.args.get('asset_type')
        print("In api '"+str(province) +"' " + "'" +str(district) + "' " + "'" + str(sub_district)+"' "+ "'" + str(asset_type)+"' " )


        prov_arg = ''
        dist_arg = ''
        sub_dist_arg = ''
        type_arg = ''
        query = {}

        if province:
            prov_arg = f'&province={province}' 
            query['province'] = province
        if district:
            dist_arg = f'&district={district}'
            query['district'] = district
        if sub_district:
            sub_dist_arg = f'&sub_district={sub_district}'
            query['sub_district'] = sub_district
        if asset_type:
            type_arg = f'&asset_type={asset_type}'
            query['asset_type'] = asset_type
        

        
        # start_id = loads(dumps(col.find({}).sort('_id', pymongo.ASCENDING)))
        # last_id = start_id[offset]['_id']
        

        pipeline = [
                {'$match': query},
                {'$sort':  {'status':1,'_id': 1}},
                {'$skip': offset},
                {'$limit': limit} ,
        ]

        pipeline_nopaginate = [
                {'$match': query},
                {'$sort':  {'_id': 1}},
                {'$count':'count'},
        ]

        data = dumps(col.aggregate(pipeline))

        total_data = loads(dumps(col.aggregate(pipeline_nopaginate)))

        if not total_data:
            total_data = [{ 'count':0}]

        last_page = total_data[0]['count']//limit + 1

        json_data = loads(data)
        # data = dumps(col.find({'_id' : {'$gte' : last_id}}).sort('_id', pymongo.ASCENDING).limit(limit))
        # count = col.find({'source' :'TMB'}).count()
       
        if query:
            if page >= last_page:
                next_url = ''
            else:
                # next_url = '/properties?limit=' + str(limit) + '&offset=' + str(offset + limit)
                next_url = '/properties?page=' + str(page + 1) + prov_arg + dist_arg + sub_dist_arg + type_arg

            if offset - limit <= 0 :
                prev_url = ''
            else:
                prev_url = '/properties?page=' + str(page - 1) + prov_arg + dist_arg + sub_dist_arg + type_arg
        else:       
            if page >= last_page:
                next_url = ''
            else:
                # next_url = '/properties?limit=' + str(limit) + '&offset=' + str(offset + limit)
                next_url = '/properties?page=' + str(page + 1) 

            if offset - limit <= 0 :
                prev_url = ''
            else:
                prev_url = '/properties?page=' + str(page - 1) 

            
        if not json_data:
            return jsonify({
                'result': 'Not found',
                'prev_url' : prev_url,
                'next_url' : next_url,
                'total': total,
                'current_page': page,
                'last_page': last_page,
                'count' : total_data[0]['count']
            })
       
        return jsonify({
            'result': json_data,
            'prev_url' : prev_url,
            'next_url' : next_url,
            'total': total,
            'current_page': page,
            'last_page': last_page,
            'count' : total_data[0]['count']
        })

   
class AssetType(Resource):
    def get(self):
        pipeline = [
                {'$group':{'_id':"$asset_type",'count':{'$sum' :1}}},
                {'$project':{'_id':0,'type':'$_id','count':1}},
                {'$sort':  {'asset_type': 1}},
               
        ]
        
           

        data = dumps(col.aggregate(pipeline))
        json_data = loads(data)

        return jsonify({
            'result': json_data,
            'type_count': len(json_data)
        })

class AddressJson(Resource):
    def get(self):
        data = []
        p_temp = ''
        a_temp = ''
        data_json = THJson()
        for province in data_json:
            for lang in data_json[province]['name']:
                dict_p  = {}
                if lang == 'th':
                    # dict_p['province'] = {'name':data_json[province]['name'][lang]}
                    p_temp = data_json[province]['name'][lang]
                    for amphoes in data_json[province]['amphoes']:
                        for lang in data_json[province]['amphoes'][amphoes]['name']:
            
                            if lang == 'th':
                                # dict_p['province']['amphoes'] = {'name':data_json[province]['amphoes'][amphoes]['name'][lang]}
                                a_temp = data_json[province]['amphoes'][amphoes]['name'][lang]

                                for tambons in data_json[province]['amphoes'][amphoes]['tambons']:
                                    for lang in data_json[province]['amphoes'][amphoes]['tambons'][tambons]['name']:
                                       
                                        if lang == 'th':
                                            
                                            # print(data_json[province]['amphoes'][amphoes]['tambons'][tambons]['name'][lang])
                                            dict_p = {
                                                    'province':{
                                                        'name':p_temp,
                                                        'amphoes': { 
                                                            'name': a_temp,  
                                                            'tambons':{
                                                                'name':data_json[province]['amphoes'][amphoes]['tambons'][tambons]['name'][lang],
                                                                'zipcode':data_json[province]['amphoes'][amphoes]['tambons'][tambons]['zipcode']
                                                                }
                                                                }
                                                        }
                                                    }
                                            data.append(dict_p)

        return data

class AddressJsonList(Resource):
    def get(self):
        data = []
        p_temp = ''        
        data_json = THJson()
        for province in data_json:
            for lang in data_json[province]['name']:
                dict_p  = {}
                if lang == 'th':
                    # dict_p['province'] = {'name':data_json[province]['name'][lang]}
                    p_temp = data_json[province]['name'][lang]
                    dict_p['province'] = {
                        'name': p_temp,
                        'amphoes':[]
                    }
                    for amphoes in data_json[province]['amphoes']:
                        for a_lang in data_json[province]['amphoes'][amphoes]['name']:
                            a_temp = {}
                            if a_lang == 'th':
                                # dict_p['province']['amphoes'] = {'name':data_json[province]['amphoes'][amphoes]['name'][lang]}

                                t_arr = []
                                for tambons in data_json[province]['amphoes'][amphoes]['tambons']:
                                    for t_lang in data_json[province]['amphoes'][amphoes]['tambons'][tambons]['name']:
                                        t_temp = {}
                                        if t_lang == 'th':
                                            t_temp = {
                                                    'name':data_json[province]['amphoes'][amphoes]['tambons'][tambons]['name'][t_lang],
                                                    'zipcode':data_json[province]['amphoes'][amphoes]['tambons'][tambons]['zipcode']
                                                    }
                                            t_arr.append(t_temp)
                                a_temp = {
                                    'name':data_json[province]['amphoes'][amphoes]['name'][a_lang],
                                    'tambons':t_arr
                                }
                                dict_p['province']['amphoes'].append(a_temp)

                                        
                    data.append(dict_p)
        return data



class AddressJsonRaw(Resource):
    def get(self):
        data_json = THJson()
        return data_json


def THJson():
    with open('./assets/thailand.json',encoding='utf8') as json_file:
        data = json.load(json_file)

    return data
