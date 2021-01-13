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
    labels = ["Golf", "Hotel", "India", "Juliet", "Kilo", "Lima"]
    if request.method=="POST":
        print("hello world")
    return render_template("admin/dashboard.html", datasets=datasets, labels=labels)
