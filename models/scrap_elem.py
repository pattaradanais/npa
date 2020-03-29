from dataclasses import dataclass, field
from typing import Dict, List
from bs4 import BeautifulSoup
import requests
import re
import uuid
import math
from common.database import Database
from models.model import Model


@dataclass(eq=False)
class ScrapElem(Model):
    collection: str = field(init=False, default="scrap_elem")
    # list_page_url: str
    # source: str
    # source_full_name: str
    source: str
    source_name: str
    url: str
    base_url: str
    item_page: str
    next_page: str
    img: str #list of dict
    gg_map: str
    price: str
    asset_type: str
    asset_code: str
    area: str
    deed_num: str
    address: str #list of dict
    contact: str
    more_detail: str 

    # dict{
    #     "tag":"",
    #     "tag_name":"",
    #     "index" : 0
    # }

    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_source(cls, source: str) -> 'ScrapElem':
        try:
            return cls.find_one_by('source', source)
        except TypeError:
            return 'Source was not found'



    def json(self) -> Dict:
        return {
            "_id": self._id,
            "source": self.source,
            'source_name': self.source_name,
            'url': self.url,
            'base_url': self.base_url,
            'item_page': self.item_page,
            'next_page': self.next_page,
            'img': self.img,
            'gg_map': self.gg_map,
            'price': self.price,
            'asset_type': self.asset_type,
            'asset_code': self.asset_code,
            'area': self.area,
            'deed_num': self.deed_num,
            'address': self.address,
            'contact': self.contact,
            'more_detail': self. more_detail,
    
        }