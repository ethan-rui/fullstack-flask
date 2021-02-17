from flask import (
    render_template,
    redirect,
    request,
    Blueprint,
    url_for,
    flash,
    wrappers,
    escape,
    jsonify,
    make_response,
)
import json
from flask_uploads import UploadSet, IMAGES
import os
from flask_login import login_required, current_user
from data.inquiries import TableInquiry
from data.users import TableUser
from services.forms.inquiry import ReplyForm
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .common_api import authorizer
from ..forms.auth import RegistrationForm
from data.users import User, TableUser
from flask_login import current_user

sgkey = "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"
endpoint = Blueprint("admin_users", __name__)
photos = UploadSet("photos", IMAGES)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    return authorizer(current_user)


@endpoint.route("/users/data_table")
def api_table_users():
    db = TableUser()
    if current_user.get_id() != "00000000-0000-0000-0000-000000000002":
        queried_entries = db.query({"role": "customer"})
        entries = [i.to_json() for i in queried_entries]
    else:
        entries = [i.to_json() for i in db.objects()]
    db.close()
    print("-- Retrieving entries for users --")
    return wrappers.Response(
        status=200,
        content_type="application/json",
        response=json.dumps(entries),
    )


@endpoint.route("/users/add/admin", methods=["POST"])
def api_add_admin():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        db = TableUser()
        """unique username & email"""
        if form.username.data not in [
            x.username for x in db.objects()
        ] and form.email.data not in [x.email for x in db.objects()]:
            user = User(
                username=form.username.data,
                password=form.password.data,
                role="admin",
                email=form.email.data,
            )
            db.insert(user)
            db.close()
            # print(form.username.data, form.email.data, form.password.data)
            flash("User has been added")
            return redirect(request.referrer)
        flash("Email or Username already in used.", category="warning")
        # print("Email or Username already in used.")
        db.close()
    return render_template("admin/users/users.html", form=form)

""""Only updates the delivery status"""
@endpoint.route("/users/update/<uid>" , methods=["GET", "POST"])
def page_update_users(uid):
    db_users = TableUser()
    user = db_users.retrieve(uid)
    db_users.close()
    curren_history_list = {}
    past_history_list = {}
    for i in user.history.keys():
        history_item = user.history[i]
        status = history_item["status"]
        if status == "Delivered":
            past_history_list[i] = history_item
        else:
            curren_history_list[i] = history_item
    return render_template(
        "admin/users/update_users.html", user=user, curren_history_list = curren_history_list, past_history_list = past_history_list, 
    )

@endpoint.route("/users/update_status" , methods=["POST"])
def api_update_status():
    req = request.get_json()

    user_id = req.get("id")
    status = req.get("status")
    date = req.get("date")

    db_users = TableUser()
    user = db_users.retrieve(user_id)
    if user.history[date]["status"] != status:
        user.history[date]["status"] = status
        resp_dic = {
        "alert_message": " has been changed to "+ status,
        }
        db_users.insert(user)
        resp = make_response(jsonify(resp_dic), 200)
        return resp
    else:
        return ("", 204)
    db_users.close()




@endpoint.route("/users")
def page_table_users():
    form = RegistrationForm(request.form)
    db = TableUser()
    entries = db.objects()
    db.close()
    """
    .objects() returns all the objects
    .dict() returns all the key value pairs {uuid:entry}
    """
    return render_template(
        "admin/users/users.html", users=entries, page_title="User Management", form=form
    )


@endpoint.route("/inquiries", methods=["GET", "POST"])
def page_table_inquiries():
    db = TableInquiry()
    inquiries = db.objects()
    db.close()
    return render_template("admin/users/inquiries.html", inquiries=inquiries)


@endpoint.route("/inquiries/<uid>", methods=["GET", "POST"])
def page_info_inquiry(uid):
    db = TableInquiry()
    inquiries = db.retrieve(uid)
    form = ReplyForm(request.form)
    # Sendgrid email reply below
    if request.method == "POST" and form.validate():
        print(form.reply.data)
        message = Mail(
            from_email="nypomsg_do_not_reply@outlook.com",
            to_emails=f"{inquiries.sender_email}",
            subject=f"RE : {inquiries.subject}",
            html_content=f"""<h3> Please do not reply to this email! For more inquiries, please send in another enquiry through our website.</h3>
            <img src="https://cdn.discordapp.com/attachments/318659727649144833/811440794225344532/main.png" alt="Botania logo" ></img>
            <p>Dear {inquiries.sender_name},</p> 
            <br>
            <p>Good news! We have looked into your inquiry and have came up with a reply. </p>
            <p>This is the reply given : </p>
            <br>
            <p>{escape(form.reply.data)}</p>
            <br>
            <p> For any further inquiries, please send in another inquiry through our website and we would be glad to serve you! </p>
            <p> Yours Sincerely, </p>
            <b> {current_user.username} </b>
            <p> Botania </p>
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


@endpoint.route("/inquiries/update/<uid>", methods=["GET", "POST"])
def page_status_update(uid):
    def check_valid(attr):
        if attr is None:
            return False
        else:
            try:
                if attr.strip(" ") == "":
                    return False
            except:
                pass
        return True

    db = TableInquiry()
    target = db.retrieve(uid)
    db.close()

    if request.method == "GET":
        dbtwo = TableInquiry()
        attribute = {"status": False}
        for key, value in attribute.items():
            if check_valid(value):
                setattr(target, key, value)
        dbtwo.insert(target)
        dbtwo.close
    return redirect(url_for(f"admin_users.page_table_inquiries"))


@endpoint.route("/inquiries/data_table")
def api_table_inquiries():
    db = TableInquiry()
    entries = [i.to_json() for i in db.objects()]
    db.close()
    print("-- Retrieving entries for inquiries. --")
    return wrappers.Response(
        status=200, content_type="application/json", response=json.dumps(entries)
    )
