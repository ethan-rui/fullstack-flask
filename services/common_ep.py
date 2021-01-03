from flask import render_template, session, request, redirect, url_for, Blueprint, flash

endpoint = Blueprint("base", __name__)

"""
blueprint endpoint
"""


@endpoint.route("/")
def page_home():
    return "home"
