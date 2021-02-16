from flask import render_template, redirect, request, Blueprint, session, url_for
import os
from flask_login.utils import login_required, current_user
from data.statistics import Settings
from data.users import User, TableUser

endpoint = Blueprint("admin_statistics", __name__)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    from .common_api import authorizer

    return authorizer(current_user)


@endpoint.route("/", methods=["GET", "POST"])
def page_dashboard(): 
    usercount = [0]
    datasets = [89, 23, 63, 13, 55, 169]
    labels = ["Seafood", "Fruits", "Dairy", "Others", "Vegetables", "Meat"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    quarter1 = ["January", "Feburary", "March"]
    quarter2 = ["April", "May", "June"]
    quarter3 = ["July", "August", "September"]
    quarter4 = ["October", "November", "December"]
    quarter1expenses = [54, 120, 74]
    quarter2expenses = [69, 1337, 420]
    quarter3expenses = [93, 21, 37]
    quarter4expenses = [320, 203, 416]
    final_count = [1]
    db_users = TableUser()
    db_users.close()
    users = db_users.objects()
    total_users = len(users)
    if request.method == "POST":
        print("hello world")
    return render_template(
        "admin/dashboard.html",
        usercount=usercount,
        datasets=datasets,
        labels=labels,
        days=days,
        quarter1=quarter1,
        quarter2=quarter2,
        quarter3=quarter3,
        quarter4=quarter4,
        quarter1expenses=quarter1expenses,
        quarter2expenses=quarter2expenses,
        quarter3expenses=quarter3expenses,
        quarter4expenses=quarter4expenses,
        final_count=final_count,
        total_users=total_users,
    )

@endpoint.route("/usercount", methods=["GET", "POST"])
def api_user_total():
    final_count = [1]
    db_users = TableUser()
    db_users.close()
    users = db_users.objects()
    total_users = len(users)
    if request.method =="POST":
        print("hello world")
    return render_template(
        "admin/dashboard.html",
        final_count=final_count,
    )


@endpoint.route("/settings", methods=["GET", "POST"])
def page_settings():
    if request.method == "POST":
        settings = Settings()
        settings.set_threshold_stock(int(request.form["stock"]))
        settings.close()
    return render_template("admin/settings.html")