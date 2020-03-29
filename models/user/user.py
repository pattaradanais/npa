import uuid
from dataclasses import dataclass, field
from typing import Dict, List


from models.model import Model
from common.database import Database
from common.utils import Utils
import models.user.errors as UserErrors
from function.get_time import now_string


@dataclass
class User(Model):
    collection: str = field(init=False, default="users")
    # main info for register
    name : str
    lastname: str
    email: str
    password: str
    # for user easy to register let user update other info after regiter success
    province: str = field(default="")  
    district: str = field(default="")
    sub_district: str = field(default="")
    salary: float = field(default=None)
    interested: list = field(default_factory=lambda: [])
    # permission: int
    create_date: str = field(default="")
    update_date: str = field(default="")
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "User":
        try:
            return cls.find_one_by('email', email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this e-mail was not found.')

    @classmethod
    def is_login_valid(cls, email: str, password: str) -> bool:
        """
        This method verifies that an e-mail/password combo (as sent by the site forms) is valid or not.
        Checks that the e-mail exists, and that the password associated to that e-mail is correct.
        :param email: The user's email
        :param password: The password
        :return: True if valid, an exception otherwise
        """
        user = cls.find_by_email(email)

        if not Utils.check_hashed_password(password, user.password):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Your email or password was wrong.")

        return True

    @classmethod
    def register_user(cls,name: str,lastname: str, email: str, password: str) -> bool:
        """
        This method registers a user using e-mail and password.
        :param email: user's e-mail (might be invalid)
        :param password: password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """


        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The e-mail does not have the right format.")
        
        try:
            cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError("The e-mail you used to register already exists.")
        except UserErrors.UserNotFoundError:
            User(name, lastname, email, Utils.hash_password(password),create_date=now_string(),update_date=now_string()).save_to_mongo()

        return True


    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name" : self.name,
            "lastname" : self.lastname,
            "email": self.email,
            "password": self.password,
            "province": self.province,
            "district": self.district,
            "sub_district": self.sub_district,
            "salary": self.salary,
            "interested": self.interested,
            "create_date": self.create_date,
            "update_date":self.update_date
        }