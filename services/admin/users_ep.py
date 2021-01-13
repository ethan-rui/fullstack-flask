from flask import render_template, redirect, request, Blueprint, session, url_for
from flask_uploads import UploadSet, IMAGES
import os
from flask_login import login_required, current_user
from data.inquiries import TableInquiry, Inquiry
from data.users import User, TableUser

endpoint = Blueprint("admin_users", __name__)
photos = UploadSet("photos", IMAGES)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    from .common_api import authorizer

    return authorizer(current_user)


@endpoint.route("users")
def page_table_users():
    db = TableUser()
    entries = db.objects()
    db.close()
    """
    .objects() returns all the objects
    .dict() returns all the key value pairs {uuid:entry}
    """
    return render_template(
        "admin/users/users.html", users=entries, page_title="User Management"
    )


@endpoint.route("/user_pages/inquiries", methods=["GET", "POST"])
def page_table_inquiries():
    db = TableInquiry()
    inquiries = db.objects()
    db.close()
    return render_template("admin/users/inquiries.html", inquiries=inquiries)