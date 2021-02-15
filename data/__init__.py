import os
import uuid
from uuid import UUID, uuid4
import pytz
import shelve
from datetime import datetime

basedir = os.getcwd()
tz = pytz.timezone("Singapore")


class Entry:
    def __init__(self, uid: str = None):
        self.__uuid = str(uuid4()) if uid == None else uid
        self.__date_created = datetime.now(tz=tz)
        self.__date_updated = datetime.now(tz=tz)

    @property
    def uuid(self) -> UUID:
        return self.__uuid

    """
    date attributes have no setters because they will be static
    """

    @property
    def date_created(self):
        return self.__date_created

    @property
    def date_updated(self):
        return self.__date_updated

    def update_timestamp(self):
        self.__date_updated = datetime.now(tz=tz)

    def to_json(self) -> dict:
        return {
            "uuid": self.__uuid,
            "date_created": self.__date_created.strftime("%b %d %Y %H:%M:%S"),
            "date_updated": self.__date_updated.strftime("%b %d %Y %H:%M:%S"),
        }


class Database:
    def __init__(self, label: str = ""):
        self.__db = shelve.open(f"{basedir}/data/db/database", flag="c", writeback=True)
        if len(self.__db) < 6:
            self.__db.clear()
            self.__db["users"] = {}
            self.__db["brands_categories"] = {}
            self.__db["products"] = {}
            self.__db["inquiries"] = {}
            self.__db["frontpage"] = {
                "carousel": {},
                "featured_products": [],
            }
            self.__db["settings"] = {"threshold_stock": 100}
        if label in [
            "users",
            "brands_categories",
            "products",
            "frontpage",
            "inquiries",
            "settings",
        ]:
            self.table = self.__db[label]
            print(f"-- Accessing {label} table. --")
        else:
            print("Table does not exist.")
        # debugging purposes

    def set_table(self, label: str):
        self.table = self.__db[label]
        print(f"-- Accessing {label} table --")

    def sub_tables(self) -> list:
        return [x for x in self.__db]

    def delete(self, value: str) -> bool:
        try:
            del self.table[value]
            return True
        except KeyError as e:
            # debugging purposes
            print(f"{e}")
            return False

    def insert(self, value: Entry) -> Entry:
        self.table[value.uuid] = value
        return value

    def clear_self(self):
        self.table = {}

    def retrieve(self, uid: str) -> Entry:
        return self.table[uid]

    def clear_all(self):
        self.__db.clear()
        self.__db.sync()
        self.__db.close()

    def __len__(self) -> int:
        return len(self.table)

    def objects(self) -> list:
        return list(self.table.values())

    def dict(self):
        return self.table

    def close(self):
        self.__db.sync()
        self.__db.close()

    def query(self, query: dict = {"": ""}, mode="exact") -> list:
        """
        modes:
        exact -> matches query to attribute value exactly
        similar -> checks if query is similar to attribute value
        """
        if mode == "exact":
            try:
                return [
                    x
                    for x in self.objects()
                    if list(query.values())[0].lower()
                    == getattr(x, list(query.keys())[0]).lower()
                ]
            except Exception as e:
                print(e)
        elif mode == "similar":
            try:
                return [
                    x
                    for x in self.objects()
                    if list(query.values())[0].lower()
                    in getattr(x, list(query.keys())[0]).lower()
                ]
            except Exception as e:
                print(e)
        else:
            raise Exception("Chosen mode of query does not exist.")
