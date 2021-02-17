from data.frontpage import TableFrontPage
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

import datetime

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

    message_array = [1]
    message = ' has been removed from cart'

    """user.cart -> {product_uuid: cart_item}"""
    invalid_products = []
    for product_uuid in user.cart:
        try:
            target = db_products.retrieve(product_uuid)
            """check if there is stock"""
            #If there is no stock
            if target.stock == 0:
                message = target.name + message + " as it is out of stock"
                message_array.append(message)
                invalid_products.append(product_uuid)


            #If there is enough stock
            elif user.cart[product_uuid].quantity <=  target.stock:
                """setting the attribute of each cart item"""
                user.cart[product_uuid].img = target.images[0]
                user.cart[product_uuid].centprice_final = target.centprice_final
                user.cart[product_uuid].calc_subtotal(centprice=target.centprice_final)
                user.cart[product_uuid].name = target.name
                total_amt += user.cart[product_uuid].subtotal

            #If there is not enough stock
            else:
                message = target.name + " only left " + str(target.stock) + " in stock"
                message_array.append(message)
                """setting the attribute of each cart item"""
                user.cart[product_uuid].quantity = target.stock
                user.cart[product_uuid].img = target.images[0]
                user.cart[product_uuid].centprice_final = target.centprice_final
                user.cart[product_uuid].calc_subtotal(centprice=target.centprice_final)
                user.cart[product_uuid].name = target.name
                total_amt += user.cart[product_uuid].subtotal
        except:
            message = "An item" + message
            message_array.append(message)
            invalid_products.append(product_uuid)

    if len(invalid_products) > 0:
        for i in invalid_products:
            del user.cart[i]
        db.insert(user)
    products = user.cart_objects()
    db.close()
    print(message_array)
    return render_template("payment/cart.html", products=products, total_amt=total_amt, message = message_array)


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

    elif len(current_user.cart) == 10:
        alert_message = "Cart is full!"

    else:
        db_products = TableProduct()
        current_stock = db_products.retrieve(product_id).stock
        db_products.close()

        alert_message = "Item added successfully"
        user.add_item_cart(
            key=product_id, value=CartItem(uuid=product_id, quantity=quantity)
        )
        current_user.add_item_cart(
            key=product_id, value=CartItem(uuid=product_id, quantity=quantity)
        )
        db.insert(user)
    db.close()

    resp_dic = {
        "item_in_cart": len(user.cart),
        "alert_message": alert_message,
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
            user.cart[product_uuid].calc_subtotal(centprice=target.centprice_final)
            user.cart[product_uuid].name = target.name
            total_amt += user.cart[product_uuid].subtotal
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


@endpoint.route("/clear_cart", methods=["POST"])
@login_required
def api_clear_cart():
    """json => {user_id: user_id, amount: amount}"""
    user_uuid = request.json["user_id"]
    amount = float(request.json["amount"]) / 100
    history_dic = {}
    new_history = {}
    products = {}
    Current_time = datetime.datetime.now()
    date = Current_time.strftime("%d/%m/%Y")
    time = Current_time.strftime("%X")[0:5]
    date_time = f"{date} {time}"
    db_users = TableUser()
    target_user = db_users.retrieve(user_uuid)
    user = db_users.retrieve(current_user.uuid)
    # placing the products into a dictionary
    for product in user.cart_objects():
        products.update({product.name: product.quantity})
    # placing the dictionary into another dictionary with the total amount and status
    history_dic["products"] = products
    history_dic["total_amt"] = amount
    history_dic["status"] = "Pending for delivery"

    old_history = target_user.history

    # removes the last history to keep the history to 6
    if len(old_history) == 10:
        old_history.popitem()

    new_history[date_time] = history_dic
    new_history.update(old_history)
    # place ^ dictionary into the user's history dictionary with the date and time as key
    target_user.history = new_history

    db_products = TableProduct()
    target_products = target_user.cart

    for i in target_products:
        """removing stock from inventory"""
        product = db_products.retrieve(i)
        sold_amount = target_products[i].quantity
        product.stock -= sold_amount
        product.quantity_sold += sold_amount
        db_products.insert(product)

    """clearing cart"""
    target_user.cart = {}
    current_user.cart = {}
    db_users.insert(target_user)

    db_products.close()
    db_users.close()
    return make_response("success", 200)


@endpoint.route("/change_quantity_cart", methods=["POST"])
@login_required
def change_quantity():
    req = request.get_json()

    product_id = req.get("id")
    quantity = int(req.get("quantity"))

    db = TableUser()
    user = db.retrieve(current_user.uuid)

    """check for current stock of product"""
    db_products = TableProduct()
    current_stock = db_products.retrieve(product_id).stock
    db_products.close()

    user.add_item_cart(
        key=product_id, value=CartItem(uuid=product_id, quantity=quantity)
    )
    db.insert(user)

    db.close()
    return ("", 204)


@endpoint.route("/delete_cart", methods=["POST"])
@login_required
def delete_cart():
    req = request.get_json()

    product_id = req.get("id")

    db = TableUser()
    user = db.retrieve(current_user.uuid)
    user.cart.pop(product_id)
    db.insert(user)
    db.close()

    resp_dic = {
        "item_in_cart": len(user.cart),
    }
    resp = make_response(jsonify(resp_dic), 200)
    return resp
