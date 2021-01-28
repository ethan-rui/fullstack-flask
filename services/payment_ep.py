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
    for product_id in user.cart.keys():
        products.append(db_products.retrieve(product_id))

    db_products.close()
    return render_template("auth/payment/cart.html", products=products)

@endpoint.route("/add_cart", methods=["POST"])
@login_required
def add_cart():
    product_id = request.form.get("product_id")
    quantity = int(request.form.get("quantity"))
    db = TableUser()
    user = db.retrieve(current_user.uuid)
    user.set_products_cart(product_id, quantity)
    current_user.set_products_cart(product_id, quantity)
    db.insert(user)
    db.close()
    return redirect(request.referrer)

@endpoint.route("/table_cart", methods=["POST"])
@login_required
def api_table_cart():
    db = TableUser()
    user = db.retrieve(current_user.uuid)
    db.close
    db_products = TableProduct()
    display = {}
    total_amt = 0
    for product_id in user.cart.keys():
        product = db_products.retrieve(product_id)
        name = product.name
        imag = product.images[0]
        price = product.centprice_final
        quantity = user.cart[product_id]
        total_amt += price * quantity
        item_product = {
            "image": imag ,
            "name": name,
            "price": price,
            "quantity": quantity
        }
        display[product_id] = item_product
    display["total_amt"] = total_amt
    db_products.close()
    return wrappers.Response(
        status=200, content_type="application/json", response=json.dumps(display)
    )

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
