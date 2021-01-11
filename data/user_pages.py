from data import Database
import os

basedir = os.getcwd()


class TableUserPages(Database):
    def __init__(self):
        label = "user_pages"
        super().__init__(label=label)
        self.label = label

    def __str__(self):
        return f"Components include\n--Front Page--\n  Carousell\n  3 promotional items\nProduct Page"

    def insert_promo(self, value: str) -> str:
        self.table["promo_products"].append(value)
        return value

    def insert_carou(self, value: str) -> str:
        self.table["carousel"].append(value)
        return value

    def remove_promo(self, value: str) -> str:
        print(self.table["promo_products"])
        self.table["promo_products"].remove(value)

    def remove_carou(self, value: str) -> str:
        self.table["carou"].remove(value)

    def show_items(self) -> dict:
        for key, value in self.table.items():
            for x in value:
                print(f"{key}: {x}")
        return


class FrontPage:
    def __init__(self, component: str = None):
        self.__carousel = {}
        """
        {slide_no:image_path}
        """
        self.__promo_products = {1: None, 2: None, 3: None}
        """ 
        {product_no:image_path}
        """

    @property
    def promo_products(self) -> dict:
        for i in range(len(self.__promo_products)):
            if (
                os.path.isfile(f"{basedir}/static/media/{self.__promo_products[i]}")
                is False
            ):
                self.__images[i] = "img_products/default_img.png"
                print(f"replace images index {i}")
        return self.__promo_products

    @promo_products.setter
    def promo_products(self, param: dict):
        print(param)
        key, value = list(param.items())[0]
        self.__promo_products[key] = value

    @property
    def carousell(self):
        for i in range(len(self.__carousel)):
            if os.path.isfile(f"{basedir}/static/media/{self.__carousel[i]}") is False:
                self.__images[i] = "img_products/default_img.png"
                print(f"replace images index {i}")
        return self.__carousel
