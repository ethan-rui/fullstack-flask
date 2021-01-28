from flask import Flask
import os
from datetime import timedelta
from flask.templating import render_template
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from flask_login import LoginManager, current_user
from werkzeug.utils import redirect
from data.users import TableUser

basedir = os.getcwd()

app = Flask(
    __name__,
    template_folder=f"{basedir}/templates",
    static_folder=f"{basedir}/static",
)
app.config["SECRET_KEY"] = "1234"
app.permanent_session_lifetime = timedelta(days=3)
app.config["UPLOADED_PHOTOS_DEST"] = f"{basedir}/static/media"
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

"""flask-login config"""
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db = TableUser()
    try:
        user = db.dict()[user_id]
    except KeyError:
        return redirect("/")
    db.close()
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("errors/401.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html")


"""other login routes under auth_ep.py"""


from services.common_ep import endpoint as EP_Common
from services.auth_ep import endpoint as EP_Auth
from services.admin.inventory_ep import endpoint as EP_Admin_Inv
from services.admin.users_ep import endpoint as EP_Admin_Users
from services.admin.statistics_ep import endpoint as EP_Admin_Stats
from services.admin.common_api import endpoint as EP_Admin_API
from services.payment_ep import endpoint as EP_Payment

# from services.admin_ep import endpoint as EP_Admin

app.register_blueprint(EP_Common, url_prefix="/")
app.register_blueprint(EP_Auth, url_prefix="/user")
app.register_blueprint(EP_Admin_Inv, url_prefix="/admin")
app.register_blueprint(EP_Admin_Users, url_prefix="/admin")
app.register_blueprint(EP_Admin_Stats, url_prefix="/admin")
app.register_blueprint(EP_Admin_API, url_prefix="/admin")
app.register_blueprint(EP_Payment, url_prefix="/user")

if __name__ == "__main__":
    from data.products import TableBC, Brand, Category
    from data.users import User, TableUser

    """
    inserting the default entries to tables before server starts
    - superuser
    - brand
    - categories
    """
    # default brands & categories
    db_bc = TableBC()
    db_bc.insert(Category(uid="1"))
    db_bc.insert(Brand(uid="0"))
    db_bc.close()
    # default superuser
    db_users = TableUser()
    db_users.insert(
        User(
            username="admin",
            password="password",
            role="admin",
            uid="0",
            email="admin@admin.com",
        )
    )
    db_users.close()

    app.run(debug=True)