from data import Database
from data.products import TableProduct
import os

basedir = os.getcwd()


class TableFrontPage(Database):
    def __init__(self):
        label = "frontpage"
        super().__init__(label)
        self.label = label

    @property
    def carousel(self):
        return self.table["carousel"]

    @property
    def featured_products(self):
        return self.table["featured_products"]

    def insert_carousel(self, img: str, index: int):
        self.table["carousel"][index] = img

    def delete_carousel(self, index: int):
        del self.table["carousel"][index]
        os.remove(f"{basedir}/static/media/img_carousel/carousel_{index}.png")
    
    def insert_featured(self, uuid: str):
        self.table["featured_products"].append(uuid)

    def delete_featured(self, uuid: int):
        self.table["featured_products"].remove(uuid)