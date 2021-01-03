from uuid import uuid4
import shelve
import os

# import your datetime, timezone modules

basedir = os.getcwd()


class Entry:
    def __init__(self, uid: str = "", name: str = "default_name"):
        self.name = name
        self.__uuid = str(uuid4()) if uid == "" else uid

    @property
    def uuid(self):
        return f"this is the uuid: {self.__uuid}"

    @uuid.setter
    def uuid(self, value: str) -> str:
        self.__uuid = value
        return value

    """
    date created, date updated
    getter & setter using the property decorator
    """


class Database:
    def __init__(self, label: str):
        labels = ["users", "products", "brands_categories"]
        if label not in labels:
            raise KeyError(f"{labels} not accepted")

        self.__db = shelve.open(
            f"{basedir}/data/db/database.db", flag="c", writeback=True
        )
        self.table = self.__db[label]

    def retrieve(self, uuid: str) -> Entry:
        return self.__table[uuid]

    def insert(self, entry: Entry) -> Entry:
        self.table[entry.uuid] = entry

    def close(self):
        self.__db.sync()
        self.__db.close()

    def delete(self, value: str) -> bool:
        try:
            del self.table[value]
            return True
        except KeyError as e:
            print(e)
            return False

    def clear_all(self):
        self.table = {}

    def __len__(self):
        return len(self.table)

    def retrieve_all(self) -> list:
        return [x for x in self.table]

    def retrieve_all_object(self) -> list:
        return [x for x in self.table.values()]
