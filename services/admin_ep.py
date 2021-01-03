from flask import render_template, session, request, redirect, url_for, Blueprint, flash

endpoint = Blueprint("admin_ep", __name__)

"""
blueprint endpoint
"""


@endpoint.route("/hello")
def page_dashboard():
    return "dashboard"


@endpoint.route("/inventory")
def page_inventory():
    y = [i for i in range(5)]
    return render_template("admin/inventory.html", y=y)
