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
    list_page_url: str
    source: str
    source_full_name: str
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
            "list_page_url": self.list_page_url,
            "source": self.source,
            "source_full_name": self.source_full_name
        }