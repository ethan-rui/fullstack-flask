from flask.signals import message_flashed
from flask.templating import render_template
from flask.wrappers import Request
from data.user_pages import TableUserPages
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
            db = Database(label=keys[table])
            target = db.retrieve(uid)
            """
            deleting images of the products
            """
            if keys[table] == "products":
                for x in list((target.images).values()):
                    if x != "img_products/default_img.png":
                        os.remove(f"{basedir}/static/media/{x}")
            db.delete(uid)
            db.close()
        if keys[table] != "users":
            return redirect(url_for(f"admin_inventory.page_table_{table}"))
        else:
            return redirect(url_for(f"admin_users.page_table_users"))


def authorizer(user):
    try:
        if user.role != "admin":
            print(f"{user.username} unauthorized.")
            return render_template("errors/403.html")
    except:
        return render_template("errors/403.html")
