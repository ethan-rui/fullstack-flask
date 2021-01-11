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


@endpoint.route("/")
def page_dashboard():
    return render_template("admin/dashboard.html")
