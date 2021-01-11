import os
from data import Database, Entry
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

basedir = os.getcwd()

# UserMixin is for flask-login
class User(Entry, UserMixin):
    def __init__(
        self,
        username: str = "",
        password: str = "",
        role: str = "customer",
        email: str = "",
        uid: str = None,
        full_address={"city": "-", "country": "-", "pcode": "-"},
    ):
        try:
            Entry.__init__(self, uid=uid)
            self.username = username
            self.email = email
            self.password = generate_password_hash(password)
            self.__full_address = full_address
            self.role = role
            print(f"Username: {self.username}")
            print(f"Password: {self.password}")
            print(f"Role: {self.role}")
            print(f"ID: {self.uuid}")
        except Exception as e:
            raise e

    def get_id(self):
        return self.uuid

    def full_address(self, value: str):
        if value == "all":
            return " ".join(list(self.__full_address.values()))
        else:
            return self.__full_address[value]

    def set_full_address(self, key, value):
        if key not in ["country", "city", "pcode"]:
            raise KeyError(f"{key} is not an attribute of full_address")
        else:
            self.__full_address[key] = value

    def password_change(self, password_old: str, password_new: str) -> bool:
        if check_password_hash(pwhash=self.password, password=password_old):
            self.password = generate_password_hash(password_new)
            self.update_timestamp()
            return True
        else:
            return False


class TableUser(Database):
    def __init__(self):
        label = "users"
        super().__init__(label=label)
        self.label = label

    def authenticate(self, username: str, password: str):
        for x in self.objects():
            if x.username == username:
                if check_password_hash(pwhash=x.password, password=password):
                    return True, x
        return False

    # def select(self, query: dict):
    #     result = []
    #     for x in query:
    #         if query[x].strip() != "" or query[x] is not None:
    #             if query[x].values() in self.table.list()
