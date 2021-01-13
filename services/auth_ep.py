from flask import render_template, session, request, redirect, url_for, Blueprint, flash
from flask_login.utils import login_required, login_user, logout_user, current_user
from .forms.auth import RegistrationForm, LoginForm, ProfileForm, PswUpdateForm
from data.users import User, TableUser

endpoint = Blueprint("auth", __name__)


@endpoint.route("/register", methods=["GET", "POST"])
def page_register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.page_profile"))
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
                role="customer",
                email=form.email.data,
            )
            db.insert(user)
            db.close()
            # print(form.username.data, form.email.data, form.password.data)
            flash("Thanks for registering")
            return redirect(url_for("auth.page_login"))
        flash("Email or Username already in used.", category="warning")
        # print("Email or Username already in used.")
        db.close()
    return render_template("auth/register.html", form=form)


@endpoint.route("/login", methods=["GET", "POST"])
def page_login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.page_profile"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            db = TableUser()
            username = form.username.data
            password = form.password.data
            authenticated, user = db.authenticate(username=username, password=password)
        except:
            flash("Invalid credentials")
            return redirect(url_for("auth.page_login"))
        print(authenticated)
        print(user)
        """
        authenticate -> (bool, user data)
        """
        db.close()
        if authenticated:
            flash("Logged in successfully")
            login_user(user)
            print("Logged in successfully")
            if user.role == "admin":
                return redirect(url_for("admin_statistics.page_dashboard"))
            else:
                return redirect(url_for("base.page_home"))
    return render_template("auth/login.html", form=form)


@endpoint.route("/logout")
@login_required
def page_logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("base.page_home"))


@endpoint.route("/profile")
@login_required
def page_profile():
    return render_template("auth/profile.html")


@endpoint.route("/profile/edit", methods=["GET", "POST"])
@login_required
def page_update_profile():
    form = ProfileForm(request.form)
    if form.validate():
        db = TableUser()
        user = db.retrieve(current_user.uuid)
        user.set_full_address(key="city", value=form.city.data)
        user.set_full_address(key="country", value=form.country.data)
        user.set_full_address(key="pcode", value=form.pcode.data)
        print(user.full_address)
        db.insert(user)
        db.close()
        flash("Your address have been updated!")
        return render_template("auth/profile.html")
    else:
        return render_template("auth/update/address.html", form=form)
    return render_template("auth/update/address.html", form=form)


@endpoint.route("/profile/password", methods=["GET", "POST"])
@login_required
def page_update_password():
    form = PswUpdateForm(request.form)
    if request.method == "POST" and form.validate():
        db = TableUser()
        user = db.retrieve(current_user.uuid)
        oldpassword = form.oldpassword.data
        password = form.password.data
        if user.password_change(password_old=oldpassword, password_new=password):
            db.insert(user)
            db.close()
            flash("Password updated successfully!")
            return redirect(url_for("auth.page_profile"))

        else:
            flash("Wrong password!")
            return render_template(
                "auth/update/password.html", form=form
            )
    return render_template("auth/update/password.html", form=form)