from flask import render_template, Blueprint, request
from werkzeug.utils import redirect
from data.frontpage import TableFrontPage
from flask_login.utils import login_required, current_user
import os
from .common_api import authorizer
from PIL import Image
from services.forms.frontpage import UpdateCarousel, UpdateFeaturedProducts
import json

endpoint = Blueprint("admin_frontpage", __name__)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    return authorizer(current_user)


@endpoint.route("/front-page/carousel", methods=["POST", "GET"])
def page_config_carousel():
    db = TableFrontPage()
    db.close()
    form = UpdateCarousel(request.form)
    if request.method == "POST":
        images = {
            0: request.files.get("image_0"),
            1: request.files.get("image_1"),
            2: request.files.get("image_2"),
            3: request.files.get("image_3"),
            4: request.files.get("image_4"),
        }
        for i in images:
            """empty fields have no filename"""
            if images[i].filename.replace(" ", "") != "":
                img = Image.open(images[i])
                img = img.resize((1200, 600))
                img.convert("RGB")
                img.save(f"{basedir}/static/media/img_carousel/carousel_{i}.png")

                db_carou = TableFrontPage()
                db_carou.insert_carousel(img=f"img_carousel/carousel_{i}.png", index=i)
                db_carou.close()
        return redirect(request.referrer)
    return render_template(
        "/admin/front_page/carousel.html", img_carousel=db.carousel, form=form
    )


@endpoint.route("/front-page/delete/<table>", methods=["POST"])
def api_delete_frontpage(table):
    tables = ["carousel", "featured"]
    if table in tables:
        """data -> the indices of the slides that are to be deleted"""
        data = [int(x) for x in request.json]
        db = TableFrontPage()
        if table == "carousel":
            for img in data:
                db.delete_carousel(img)
        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@endpoint.route("/front-page/featured")
def page_config_featured_products():
    return render_template("/admin/front_page/featured_products.html")