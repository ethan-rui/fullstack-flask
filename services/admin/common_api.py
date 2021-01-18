from flask.signals import message_flashed
from flask.templating import render_template
from flask.wrappers import Request
from data.user_pages import TableUserPages
from data.inquiries import TableInquiry
from flask import Blueprint, wrappers, url_for, redirect, request
from data import Database
import os

basedir = os.getcwd()
endpoint = Blueprint("api", __name__)


@endpoint.route("delete/<table>/<uid>", methods=["POST"])
def api_delete(table, uid):
    # {page_name: table name}
    if request.method == "POST":
        keys = {
            "brands": "brands_categories",
            "categories": "brands_categories",
            "products": "products",
            "users": "users",
            "user_pages": "user_pages",
            "inquiries": "inquiries",
        }
        """
        uuid4() generates string of len 36,
        only able to delete objects with uuid4
        """
        if table not in keys.keys():
            return "not found"

        """
        different types of deletion
        """
        if table == "user_pages" and len(uid) == 36:
            db = TableUserPages()
            try:
                print(db.remove_promo(uid))
            except:
                print(f"{uid} does not exists in user_pages")
            db.close()
            return redirect(url_for(f"admin_userpages.page_update_promo"))

        if len(uid) == 36:
            # setting the brands & categories of other products to default
            if keys[table] == "brands_categories":
                db_products = Database(label="products")
                for x in db_products.objects():
                    if x.brand == uid:
                        x.brand == 0
                        db_products.insert(x)
                    if x.cat == uid:
                        x.cat == 1
                        db_products.insert(x)
                db_products.close()

            # deleting the images of products
            db = Database(label=keys[table])

            target = db.retrieve(uid)
            if keys[table] == "products":
                for x in list((target.images).values()):
                    if x != "img_products/default_img.png":
                        os.remove(f"{basedir}/static/media/{x}")

            db.delete(uid)
            db.close()

            return redirect(request.referrer)


def authorizer(user):
    try:
        if user.role != "admin":
            print(f"{user.username} unauthorized.")
            return render_template("errors/403.html")
    except:
        return render_template("errors/403.html")
