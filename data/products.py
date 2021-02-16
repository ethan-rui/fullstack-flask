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
        sold = 0,
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
        self.__images = {0: None, 1: None, 2: None}
        self.sold = sold

    @property
    def images(self) -> dict:
        for i in range(len(self.__images)):
            if os.path.isfile(f"{basedir}/static/media/{self.__images[i]}") is False:
                self.__images[i] = "placeholders/placeholder.png"
                print(f"Replacing images index {i}")
        return self.__images

    @property
    def centprice_final(self):
        return self.centprice * ((100 - self.discount) / 100)

    @images.setter
    def images(self, param: dict):
        print(param)
        key, value = list(param.items())[0]
        self.__images[key] = value

    def to_json(self) -> dict:
        return {
            **(super().to_json()),
            "name": self.name,
            "brand": self.brand,
            "cat": self.cat,
            "image": self.images[0],
            "stock": self.stock,
            "price": f"{(self.centprice/100):.2f}",
            "discount": self.discount,
            "price_final": f"{(self.centprice_final/100):.2f}",
            "desc": self.desc,
        }


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

    def to_json(self) -> dict:
        return {**(super().to_json()), "name": self.name, "desc": self.desc}


class TableBC(Database):
    def __init__(self):
        label = "brands_categories"
        super().__init__(label)
        self.label = label


class CartItem:
    def __init__(self, uuid: str, quantity: int):
        self.__uuid = uuid
        self.quantity = quantity

        """set by the page_cart, so its always up to date with db"""
        self.__subtotal = 0
        self.name = ""
        self.img = ""

    @property
    def uuid(self):
        return self.__uuid

    def calc_subtotal(self, centprice: int):
        self.__subtotal = self.quantity * centprice

    @property
    def subtotal(self):
        return self.__subtotal
