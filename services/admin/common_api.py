from flask.signals import message_flashed
from flask.templating import render_template
from flask.wrappers import Request
from data.inquiries import TableInquiry
from flask import Blueprint, wrappers, url_for, redirect, request
from data import Database, Entry
import os

basedir = os.getcwd()
endpoint = Blueprint("api", __name__)


@endpoint.route("delete/<table>/<uid>", methods=["POST"])
def api_delete(table, uid):
    print("-- deleting --")
    # {page_name: table name}
    if request.method == "POST":

        def del_products(target: Entry):
            print("-- deleting products --")
            for x in list((target.images).values()):
                if x != "img_products/default_img.png":
                    os.remove(f"{basedir}/static/media/{x}")

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
        }

        if table not in function_delete.keys():
            print("Table was not found, redirecting back to main page.")
            return redirect(request.referrer)
        else:
            """
            object specific functions
            """
            db = Database(label=table)
            try:
                target = db.retrieve(uid)
            except:
                pass

            if table == "products":
                function_delete[table](target)
                print("-- deleting by object --")
            else:
                function_delete[table](uid)
                print("-- deleting by uuid -- ")
            """
            universal functions
            """
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
