from flask import render_template, redirect, request, Blueprint, session, url_for
import os
from flask_login.utils import login_required, current_user

endpoint = Blueprint("admin_statistics", __name__)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    from .common_api import authorizer

    return authorizer(current_user)


@endpoint.route("/", methods=["GET", "POST"])
def page_dashboard():
    datasets = [89, 23, 63, 13, 55, 169]
    labels = ["Apple", "Orange", "Fish", "Brinjal", "Banana", "Pineapple"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    quarter1 = ["January", "Feburary", "March"]
    quarter2 = ["April", "May", "June"]
    quarter3 = ["July", "August", "September"]
    quarter4 = ["October", "November", "December"]
    quarter1expenses = ["January", "Feburary", "March"]
    quarter2expenses = ["April", "May", "June"]
    quarter3expenses = ["July", "August", "September"]
    quarter4expenses = ["October", "November", "December"]
    if request.method == "POST":
        print("hello world")
    return render_template("admin/dashboard.html", datasets=datasets, labels=labels, days=days, quarter1=quarter1, quarter2=quarter2, quarter3=quarter3, quarter4=quarter4)
