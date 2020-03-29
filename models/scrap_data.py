from dataclasses import dataclass, field
from typing import Dict, List
from bs4 import BeautifulSoup
import requests
import re
import uuid
import math

from common.database import Database
from models.model import Model
from models.scrap_elem import ScrapElem
from function.address_check import address_check
from function.get_time import now_string
from function.str_concat import str_concat, str_concat_nospace, str_concat_comma
from function.area_split import area_split


@dataclass(eq=False)
class Scrap(Model):

    collection: str = field(init=False, default="properties")


    source: str
    # source_full: str
    asset_url: str
    asset_img: list #url list
    # draw_map: list
    gg_map: str
    price: str
    asset_type: str
    asset_code: str
    area: str
    area_rai: float
    area_ngan: float
    area_sq_wa: float
    deed_num: str
    address: str
    province: str
    district :str
    sub_district: str
    contact: str
    more_detail: str
    update_date: str
    scrap_date: str

    
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    # def load_property(self) -> float:
    #     request = requests.get(self.url)
    #     content = request.content
    #     soup = BeautifulSoup(content, "html.parser")
    #     element = soup.find(self.tag_name, self.query)
    #     string_price = element.text.strip()

    #     pattern = re.compile(r"(\d+,?\d+\.\d+)")
    #     match = pattern.search(string_price)
    #     found_price = match.group(1)
    #     without_commas = found_price.replace(",", "")
    #     self.price = float(without_commas)
    #     return self.price


                
    @classmethod
    def find_by_property_id(cls,property_id: str):
        return cls.find_one_by('property_id', property_id)

    @classmethod
    def get_raw_data(cls):
        return cls.all_by_collection("raw_data") 

    @classmethod
    def integrateData(cls):
        # raw = self.get_raw_data()
        raw = Database.find('raw_data',{})
        for data in raw:
            _id = data['_id']
            source = data['source']
            asset_url = data['url'] 
            asset_img = data['img']
            try:
                gg_map = data['gg_map'][0]
            except:
                gg_map = "Google map not found"
            price = str_concat_nospace(data['price']).strip()
            asset_type = str_concat_nospace(data['asset_type'])
            asset_code = str_concat_nospace(data['asset_code'])

            area_dict = area_split(str_concat_nospace(data['area'])) 
            area = data['area'][0]
            area_rai = float(area_dict['rai'])
            area_ngan = float(area_dict['ngan'])
            area_sq_wa = float(area_dict['sq_wa'])

            deed_num = str_concat(data['deed_num'])
            address = str_concat(data['address'])
            address = address.strip()
            address_dict = address_check(address)
            province = address_dict['province']
            district = address_dict['district']
            sub_district = address_dict['sub_district']

            contact = str_concat_comma(data['contact']) 
            more_detail = str_concat(data['more_detail'])
            scrap_date = data['scraping_date'] 

            print(_id)

            Scrap(
                _id=_id,
                source=source,
                asset_url=asset_url,
                asset_img=asset_img,
                gg_map=gg_map,
                price=price,
                asset_type=asset_type,
                asset_code=asset_code,
                area=area,
                area_rai=area_rai,
                area_ngan=area_ngan,
                area_sq_wa=area_sq_wa,
                deed_num=deed_num,
                address=address,
                province=province,
                district=district,
                sub_district=sub_district,
                contact=contact,
                more_detail=more_detail,
                update_date=now_string(),
                scrap_date=scrap_date
                ).save_to_mongo()
        return "Update success"



    def json(self) -> Dict:
        return {
            "_id": self._id,
            "source": self.source,
            "asset_url": self.asset_url,
            "asset_img": self.asset_img,
            "gg_map": self.gg_map,
            "price": self.price,
            "asset_type": self.asset_type,
            "asset_code": self.asset_code,
            "area": self.area,
            "area_rai": self.area_rai,
            "area_ngan":self.area_ngan,
            "area_sq_wa":self.area_sq_wa,
            "deed_num": self.deed_num,
            "address":self.address,
            "province":self.province,
            "district":self.district,
            "sub_district": self.sub_district,
            "contact":self.contact,
            "more_detail":self.more_detail,
            "scrap_date":self.scrap_date,
            "update_date": self.update_date,
        }

        # db.properties.insert({
        #     "_id": "0000000000000",
        #     "source": "dummy",
        #     "source_full_name": "dummy",
        #     "source_url": "dummy",
        #     "source_tel": "dummy",
        #     "img_list": ["dummy"],
        #     "map_img_list": ["dummy"],
        #     "property_type": "dummy",
        #     "property_id": "dummy",
        #     "entry_price": "dummy", 
        #     "size_full": "dummy",
        #     "size_rai": 0,
        #     "size_ngan": 0,
        #     "size_sq_wa": 0,
        #     'deed_number': "dummy"
 
        # })