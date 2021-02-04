from flask import render_template, session, request, redirect, url_for, Blueprint, flash, jsonify, make_response
from flask_login.utils import login_required, login_user, logout_user, current_user
from .forms.auth import RegistrationForm, LoginForm, ProfileForm, PswUpdateForm
from data.users import User, TableUser
from data.products import TableProduct

endpoint = Blueprint("payment", __name__)

@endpoint.route("/cart", methods=["GET", "POST"])
@login_required
def page_cart():
    db = TableUser()
    user = db.retrieve(current_user.uuid)
    db.close
    db_products = TableProduct()
    products = []
    total_amt = 0

    for product_id in user.cart.keys():
        product = db_products.retrieve(product_id)
        total_amt += product.centprice_final*user.cart[product_id]
        products.append(product)

    db_products.close()
    return render_template("payment/cart.html", products=products, total_amt = total_amt)

@endpoint.route("/add_cart", methods=["POST"])
@login_required
def add_cart():
    req = request.get_json()


    product_id = req.get("id")
    quantity = int(req.get("quantity"))

    db = TableUser()
    user = db.retrieve(current_user.uuid)
    if product_id in user.cart.keys():
        alert_message = "Item is already in cart"
        alert_color = "alert alert-warning"

    elif len(current_user.cart) == 10:
        alert_message = "Cart is full!"
        alert_color = "alert alert-warning"

    else:
        alert_message = "Item added successfully"
        alert_color = "alert alert-success"
        user.set_products_cart(product_id, quantity)
        current_user.set_products_cart(product_id, quantity)
        db.insert(user)
    db.close()

    resp_dic = {"item_in_cart": len(current_user.cart), "alert_message": alert_message, "alert_color": alert_color}

    resp = make_response(jsonify(resp_dic), 200)

    return resp

@endpoint.route("/checkout", methods=["POST"])
@login_required
def api_checkout():
    db = TableUser()
    user = db.retrieve(current_user.uuid)
    current_user.cart = {}
    user.cart = {}
    db.insert(user)
    db.close()
    flash("Payment Completed")
    return render_template("common/home.html")
