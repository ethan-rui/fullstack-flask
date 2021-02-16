from flask.templating import render_template
from flask import Blueprint, redirect, request, wrappers
from data import Database, Entry
from data.statistics import Settings
from data.products import TableProduct
import os
import json


basedir = os.getcwd()
endpoint = Blueprint("api", __name__)


@endpoint.route("delete/<table>", methods=["POST"])
def api_delete(table):
    """
    data -> list of uuids
    """
    data = request.json

    def del_products(target: Entry):
        print("-- deleting products --")
        for x in list((target.images).values()):
            if x != "img_products/default_img.png":
                try:
                    os.remove(f"{basedir}/static/media/{x}")
                except:
                    print("Can't delete placeholder image.")

    def set_defaults(uid: str):
        db_products = Database(label="products")
        for x in db_products.objects():
            if x.brand == uid:
                x.brand = 0
                db_products.insert(x)
            if x.cat == uid:
                x.cat = 1
                db_products.insert(x)
        # only inserts the object if there are any changes
        db_products.close()

    function_delete = {
        "products": del_products,
        "brands_categories": set_defaults,
        "users": print,
        "inquiries": print,
    }

    if table not in function_delete.keys():
        print("Table was not found, redirecting back to main page.")
    else:
        """
        object specific functions
        """
        db = Database(label=table)
        for entry in data:
            try:
                target = db.retrieve(entry)
            except:
                return redirect(request.referrer)
            else:
                if table == "products":
                    function_delete[table](target)
                    print("-- deleting by object --")
                else:
                    function_delete[table](entry)
                    print("-- deleting by uuid -- ")
                    """
                    universal functions
                    """
                db.delete(entry)
        db.close()
        return redirect(request.referrer)


def authorizer(user):
    try:
        if user.role != "admin":
            print(f"{user.username} unauthorized.")
            return render_template("errors/403.html")
    except:
        return render_template("errors/403.html")


@endpoint.route("/notifications")
def collate_notif():
    settings = Settings()
    """collect params for displaying notif"""
    threshold_stock = settings.get_threshold_stock()
    print(threshold_stock)
    """filter products"""
    db_products = TableProduct()
    low_stock_products = [
        (x.name, x.stock, x.uuid)
        for x in db_products.objects()
        if x.stock <= threshold_stock
    ]

    invalid_img_products = []
    """products with invalid images"""
    for i in db_products.objects():
        for j in i.images:
            if i.images[j] == "placeholders/placeholder.png":
                invalid_img_products.append((i.name, i.uuid))
                break

    products_notif = invalid_img_products + low_stock_products
    db_products.close()
    settings.close()
    return wrappers.Response(
        status=200, content_type="application/json", response=json.dumps(products_notif)
    )
