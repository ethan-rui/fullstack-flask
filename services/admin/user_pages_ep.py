from flask import render_template, redirect, request, Blueprint, session, url_for
from flask_uploads import UploadSet, IMAGES
import os
from flask_login import login_required, current_user
import data
from data.products import TableProduct, TableBC
from data import Database
from data.user_pages import TableUserPages, FrontPage
from ..forms.front_page import UpdateCarousel, UpdatePromoProducts

endpoint = Blueprint("admin_userpages", __name__)
photos = UploadSet("photos", IMAGES)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    from .common_api import authorizer

    return authorizer(current_user)


@endpoint.route("/user_pages/update/front_page/promo_products", methods=["GET", "POST"])
def page_update_promo():
    db = Database()
    db.set_table("products")
    products = db.list_objects()
    product_keys = db.list_keys()

    db.set_table("brands_categories")
    bc = db.list_keys()

    db.set_table("user_pages")
    promo = db.list_keys()["promo_products"]

    db.close()

    if request.method == "POST":
        db = TableUserPages()
        value = request.form["uuid"]
        db.insert_promo(value)
        db.close()
        return redirect(url_for("admin_userpages.page_update_promo"))

    return render_template(
        "admin/user_pages/promo_items.html",
        products=products,
        product_keys=product_keys,
        bc=bc,
        page_title="Promotion Items",
        promo=promo,
    )


@endpoint.route("/user_pages/update/front_page/carousel", methods=["GET", "POST"])
def page_update_carousel():
    form = UpdateCarousel()
    db = TableUserPages()
    data_carousel = db.list_keys()["carousel"]
    db.close()
    return render_template(
        "admin/user_pages/carousel.html",
        data_carousel=data_carousel,
        form=form,
    )
