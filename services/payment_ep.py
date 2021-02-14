from flask import (
    render_template,
    session,
    request,
    redirect,
    url_for,
    Blueprint,
    flash,
    jsonify,
    make_response,
)
from flask_login.utils import login_required, login_user, logout_user, current_user
from .forms.auth import RegistrationForm, LoginForm, ProfileForm, PswUpdateForm
from data.users import User, TableUser
from data.products import TableProduct, CartItem

endpoint = Blueprint("payment", __name__)


@endpoint.route("/cart", methods=["GET", "POST"])
@login_required
def page_cart():
    db = TableUser()
    user = db.retrieve(current_user.uuid)
    """check if cart is empty"""
    if len(user.cart) == 0:
        db.close()
        return render_template("payment/cart.html")

    db_products = TableProduct()
    db_products.close()

    """"{products name: quantity}"""
    total_amt = 0

    """user.cart -> {product_uuid: cart_item}"""
    invalid_products = []
    for product_uuid in user.cart:
        try:
            target = db_products.retrieve(product_uuid)
            """setting the attribute of each cart item"""
            user.cart[product_uuid].img = target.images[0]
            user.cart[product_uuid].centprice_final = target.centprice_final
            user.cart[product_uuid].calc_subtotal(centprice=target.centprice)
            user.cart[product_uuid].name = target.name
            total_amt += target.centprice_final
        except:
            invalid_products.append(product_uuid)

    if len(invalid_products) > 0:
        for i in invalid_products:
            del user.cart[i]
        db.insert(user)
    products = user.cart_objects()
    db.close()
    return render_template("payment/cart.html", products=products, total_amt=total_amt)


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
        user.add_item_cart(
            key=product_id, value=CartItem(uuid=product_id, quantity=quantity)
        )
        current_user.add_item_cart(
            key=product_id, value=CartItem(uuid=product_id, quantity=quantity)
        )
        db.insert(user)
    db.close()

    resp_dic = {
        "item_in_cart": len(current_user.cart),
        "alert_message": alert_message,
        "alert_color": alert_color,
    }

    resp = make_response(jsonify(resp_dic), 200)
    return resp


@endpoint.route("/checkout")
@login_required
def page_checkout():
    db = TableUser()
    user = db.retrieve(current_user.uuid)
    if len(user.cart) == 0:
        db.close()
        return render_template("payment/cart.html")

    db_products = TableProduct()
    db_products.close()

    """"{products name: quantity}"""
    total_amt = 0

    """user.cart -> {product_uuid: cart_item}"""
    invalid_products = []
    for product_uuid in user.cart:
        try:
            target = db_products.retrieve(product_uuid)
            """setting the attribute of each cart item"""
            user.cart[product_uuid].img = target.images[0]
            user.cart[product_uuid].centprice_final = target.centprice_final
            user.cart[product_uuid].calc_subtotal(centprice=target.centprice)
            user.cart[product_uuid].name = target.name
            total_amt += target.centprice_final
        except:
            invalid_products.append(product_uuid)

    if len(invalid_products) > 0:
        for i in invalid_products:
            del user.cart[i]
        db.insert(user)

    products = user.cart_objects()
    db.close()
    return render_template(
        "payment/checkout.html", user=user, products=products, total_amt=total_amt
    )
