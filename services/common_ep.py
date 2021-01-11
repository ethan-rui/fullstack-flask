from flask import render_template, redirect, url_for, Blueprint
from data.user_pages import TableUserPages
from data.products import TableBC, TableProduct
endpoint = Blueprint("base", __name__)


@endpoint.route("/")
def page_home():
    # featured products -> uuid of products
    db_featured = TableUserPages()
    promo_products = db_featured.dict()["promo_products"]
    db_featured.close()

    # existing products
    db_products = TableProduct()
    promo_products_data = [db_products.dict()[i] for i in promo_products]
    db_products.close()

    # uuid to crossreference the product
    db_bc = TableBC()
    brands = [x for x in db_bc.objects() if x.role == "brand"]
    categories = [x for x in db_bc.objects() if x.role == "category"]
    db_bc.close()

    return render_template("common/home.html", 
    products=promo_products_data, 
    cats=categories, brands=brands)
