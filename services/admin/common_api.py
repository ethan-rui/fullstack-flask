from flask.templating import render_template
from flask import Blueprint, redirect, request
from data import Database, Entry
import os

basedir = os.getcwd()
endpoint = Blueprint("api", __name__)


@endpoint.route("delete/<table>", methods=["POST"])
def api_delete(table):
    """
    data = [uuid, uuid, uuid]
    """
    data = request.json

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


# @endpoint.route("delete/<table>/<uid>", methods=["POST"])
# def api_delete_inquiry(table, uid):
#     """
#     data = [uuid, uuid, uuid]
#     """


#     function_delete = {
#         "inquiries": print
#     }

#     if table not in function_delete.keys():
#         print("Table was not found, redirecting back to main page.")
#     else:
#         """
#         object specific functions
#         """
#         db = Database(label=table)
#         if table == "inquiries":
#             target = db.retrieve(uid)
#             function_delete[table](uid)
#             print("-- deleting by uuid --")
#             db.delete(uid)
#         db.close()
#         return redirect("/admin/inquiries")