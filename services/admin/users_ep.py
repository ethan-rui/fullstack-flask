from flask import render_template, redirect, request, Blueprint, session, url_for
from flask_uploads import UploadSet, IMAGES
import os
from flask_login import login_required, current_user
from data.inquiries import TableInquiry, Inquiry
from data.users import User, TableUser
from services.forms.inquiry import ReplyForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sgkey = "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"
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


@endpoint.route("/user_pages/inquiry/<uid>", methods=["GET", "POST"])
def page_info_inquiry(uid):
    db = TableInquiry()
    inquiries = db.retrieve(uid)
    print(inquiries.sender_name)
    form = ReplyForm(request.form)
    if request.method == "POST" and form.validate():
        print(form.reply.data)
        message = Mail(
            from_email="nypomsg_do_not_reply@outlook.com",
            to_emails=f"{inquiries.sender_email}",
            subject=f"RE : {inquiries.subject}",
            html_content=f"""<h3> Please do not reply to this email! For more inquiries, please send in another enquiry through our website.</h3>
            <p>Dear {inquiries.sender_name},</p> 
            <br>
            <p>Good news! We have looked into your inquiry and have came up with a reply. </p>
            <p>This is the reply given : </p>
            <br>
            <p>{form.reply.data}</p>
            <br>
            <p> For any further inquiries, please send in another inquiry through our website and we would be glad to serve you! </p>
            <p> Yours Sincerely, </p>
            <b> Admin </b>
            <p> Online Market SG </p>
            <p> (This is an automatically-generated email, please do not reply)</p>
            <b><i> Disclaimer : You are receiving this email because you have chosen to register for us under this email address. \n If you are not the intended receipient, you may ignore this email. </i></b>""",
        )
        try:
            sg = SendGridAPIClient(sgkey)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(f"Sendgrid error : {e}")
        return redirect(url_for("admin_users.page_table_inquiries"))
    db.close()
    return render_template(
        "admin/users/info_inquiry.html", inquiries=inquiries, form=form
    )
