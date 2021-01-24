from data import Entry, Database
import os
import os.path

basedir = os.getcwd()


class Product(Entry):
    def __init__(
        self,
        name: str,
        brand: str = "default_brand",
        category: str = "default_category",
        stock: int = 0,
        desc: str = "product_desccription",
        centprice: int = 0,
        discount: int = 0,
        uid: str = None,
    ):
        super().__init__(uid)
        self.name = name
        self.brand = brand
        self.cat = category
        self.centprice = centprice
        self.stock = stock
        self.desc = desc
        self.discount = discount
        self.role = "products"
        self.__images = {1: None, 2: None, 3: None}

    @property
    def images(self) -> dict:
        for i in range(len(self.__images)):
            if os.path.isfile(f"{basedir}/static/media/{self.__images[i]}") is False:
                self.__images[i] = "img_products/default_img.png"
                print(f"replace images index {i}")
        return self.__images

    @images.setter
    def images(self, param: dict):
        print(param)
        key, value = list(param.items())[0]
        self.__images[key] = value


class TableProduct(Database):
    def __init__(self):
        label = "products"
        super().__init__(label)
        self.label = label


class Brand(Entry):
    def __init__(
        self,
        name: str = "Default Brand",
        desc: str = "-",
        link: str = "-",
        uid: str = None,
    ):
        super().__init__(uid)
        self.name = name
        self.desc = desc
        self.link = link
        self.role = "brand"

    def to_json(self) -> dict:
        return {**(super().to_json()), "name": self.name, "desc": self.desc}


class Category(Entry):
    def __init__(
        self,
        name: str = "Default Category",
        desc: str = "-",
        link: str = "-",
        uid: str = None,
    ):
        super().__init__(uid)
        self.name = name
        self.desc = desc
        self.link = link
        self.role = "cat"


class TableBC(Database):
    def __init__(self):
        label = "brands_categories"
        super().__init__(label)
        self.label = label
