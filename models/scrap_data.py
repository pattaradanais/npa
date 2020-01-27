from dataclasses import dataclass, field
from typing import Dict, List
from bs4 import BeautifulSoup
import requests
import re
import uuid
import math
from datetime import datetime
from common.database import Database
from models.model import Model
from models.scrap_elem import ScrapElem


@dataclass(eq=False)
class Scrap(Model):
    now = datetime.now()
    now_string = now.strftime("%d/%m/%Y %H:%M:%S")
    collection: str = field(init=False, default="properties")
    
    # item_page_url: str
    source: str
    source_full_name: str
    source_url: str
    source_tel: str
    img_list: List
    map_img_list: List
    property_type: str
    property_id: str
    entry_price: str
    size_full: str
    size_rai: float
    size_ngan: float
    size_sq_wa: float
    deed_number: str
    # address: str
    update_date: str = field(default=now_string)


    
    
    
    
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
    def scrap_tmb(cls, item_url: str, source: str) -> 'Scrap':
        req = requests.get(item_url)
        soup = BeautifulSoup(req.content, "html.parser")
        p = soup.find_all('p') # all <p> tag
        imgs = soup.find_all('img') #all img tag
        list = [] #for p string list
        img_list = []
        map_img_list = []
        for item in p:
            list.append(item.string)

        
        try :
            cls.find_by_property_id(list[3])  
        except:
            source_url = item_url #send
            source_full_name = ScrapElem.find_by_source(source).source_full_name
            for img in imgs:
                if 'gallery' in img.get('src'):
                    img_list.append(img.get('src'))

                if 'map' in img.get('src'):
                    map_img_list.append(img.get('src'))

            # p = soup.find_all('p')
            # for item in p:
            #     list.append(item.string)
            property_type = list[2] #send
            property_id = list[3] #send

            size = str(list[4]).split(" ")[0]
            size_split = size.split("-") #ex ['0000', '0', '52.0']
            size_full = size  #ex '0000-0-52.0' #send
            if len(size_split) == 3:
                size_rai = size_split[0] #ex '0000' #send
                size_ngan = size_split[1] #ex '0' #send
                size_sq_wa = size_split[2] #ex '52.0' #send
            else:
                size_rai = size_split[0] #ex '0000' #send
                size_ngan = 0 #ex '0' #send
                size_sq_wa = size_split[1] #ex '52.0' #send
                deed_number = list[5]
                # address = list[6]
            """
        -->0     [None,  not use
        -->1     'ราคาประกาศขาย', not use
        -->2     'บ้าน',     'property_type'
        -->3     'B12284',  'properelse
        ฤกษ์ลดา ปิ่นเกล้า-สาย 5  ซอย 8 ถนนบรมราชชนนี ต.บางเตย อ.สามพราน นครปฐม  ',
            store full 'address' and split 'province', 'destrict' ,'sub-district'

            """
            price = soup.find('div','entry-price')
            entry_price = price.contents[0] #send
            tel = soup.find('div','inline-tel')
            source_tel =  tel.a.string  #send
            Scrap(source, source_full_name, source_url, source_tel, img_list, map_img_list, property_type, property_id, entry_price, size_full, size_rai, size_ngan, size_sq_wa, deed_number,cls.now_string).save_to_mongo()
            

                                            
    @classmethod
    def scrap_one(cls, list_page_url: str, source: str) -> "Scrap":
        if source == 'tmb':
            r = requests.get(list_page_url)
            soup = BeautifulSoup(r.content, "html.parser")
            list_all = soup.find('div','search-result')
            list_all = list_all.find('span')
            list_all = int(list_all.text)
            page_all = int(math.ceil(list_all/6.0))
            first_page = soup.find_all('ul','pagination')
            first_page_url = first_page[0].a.get('href')[:-1]
            for page in range(1,page_all+1):
                r = requests.get(first_page_url+str(page))
                soup = BeautifulSoup(r.content, "html.parser")
                all_div = soup.find_all('div','entry-caption')
                for div in all_div:  #list all <div> with class='entry-caption' item html
                    #find a for get property item url ex : 'https://www.tmbbank.com/property/property/detail/B12445
                    item_url = div.find('a').get('href').encode('ascii','ignore') 
                    cls.scrap_tmb(item_url,source)

            return True
                    
                    
    
        elif source == 'ktb':
            pass
        elif source == 'led':
            pass
        elif source == 'kbank':
            pass

    # @classmethod
    # def scrap_all(cls, list_page_url: str, source: str):
    #     r = requests.get(list_page_url)
    #     soup = BeautifulSoup(r.content, "html.parser")
    #     list_all = soup.find('div','search-result')
    #     list_all = list_all.find('span')
    #     list_all = int(list_all.text)
    #     page_all = int(math.ceil(list_all/6.0))
    #     for page in range(1,page_all+1):
    #         r = requests.get(list_page_url[:-1]+str(page))
    #         soup = BeautifulSoup(r.content, "html.parser")
    #         all_div = soup.find_all('div','entry-caption')
    #         for div in all_div:  #list all <div> with class='entry-caption' item html
    #             #find a for get property item url ex : 'https://www.tmbbank.com/property/property/detail/B12445
    #             item_url = div.find('a').get('href').encode('ascii','ignore') 
    #             cls.scrap_one(item_url,source)
                
    @classmethod
    def find_by_property_id(cls,property_id: str):
        return cls.find_one_by('property_id', property_id)

   



    def json(self) -> Dict:
        return {
            "_id": self._id,
            "source": self.source,
            "source_full_name": self.source_full_name,
            "source_url": self.source_url,
            "source_tel": self.source_tel,
            "img_list": self.img_list,
            "map_img_list": self.map_img_list,
            "property_type": self.property_type,
            "property_id": self.property_id,
            "entry_price": self.entry_price, 
            "size_full": self.size_full,
            "size_rai": self.size_rai,
            "size_ngan": self.size_ngan,
            "size_sq_wa": self.size_sq_wa,
            'deed_number': self.deed_number,
            # "address": self.address
 
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