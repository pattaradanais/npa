from typing import List, Dict, TypeVar, Type
from abc import ABCMeta, abstractmethod
from datetime import datetime
from common.database import Database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    def new_to_mongo(self):
        Database.insert(self.collection, self.json())

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    # @classmethod
    # def getTime(self):
    #     now = datetime.now()
    #     now_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #     return now_string

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def all_by_collection(cls: Type[T], collection: str) -> List[T]:
        elements_from_db = Database.find(collection, {})
        return [cls(**elem) for elem in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: str) -> T:
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls: Type[T], attribute: str, value: str) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]
