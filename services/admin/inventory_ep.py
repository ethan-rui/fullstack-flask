from flask import (
    render_template,
    redirect,
    request,
    Blueprint,
    session,
    url_for,
    flash,
    wrappers,
)
from flask_login.utils import login_required, current_user
from data.products import Product, TableProduct, Brand, Category, TableBC
from data import Database
from ..forms.inventory import AddProduct, AddBrand, AddCategory, UpdateProduct
import os
from PIL import Image
import json

endpoint = Blueprint("admin_inventory", __name__)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    from .common_api import authorizer

    return authorizer(current_user)


@endpoint.route("/inventory/update/brands_categories/<uid>")
def page_update_bc(uid):
    db_bc = TableBC()
    try:
        target = db_bc.retrieve(uid)
    except:
        flash("UUID does not exists in database.")
        return redirect(url_for("admin_inventory.page_table_brands"))
    finally:
        db_bc.close()

    """param to query to database"""
    db_products = TableProduct()
    affliated_products = db_products.query({"brand": uid})
    db_products.close()
    len_affliated_products = len(affliated_products)

    return render_template(
        "admin/inventory/update/brands.html",
        target=target,
        len_affliated_products=len_affliated_products,
    )


@endpoint.route("inventory/update/brands_categories/<uid>", methods=["GET", "POST"])
def api_update_bc(uid):
    if request.method == "POST":
        db = TableBC()
        target = db.retrieve(uid)
        target.name = request.form["name"]
        target.desc = request.form["desc"]
        db.insert(target)
        db.close()
        print("Updated successful!")
        return redirect(request.referrer)


@endpoint.route("/inventory/categories", methods=["GET", "POST"])
def page_table_categories():
    form = AddCategory()
    if request.method == "POST" and form.validate_on_submit():
        cat = Category(name=form.name.data, desc=form.desc.data)
        db = TableBC()
        db.insert(cat)
        db.close()
    return render_template(
        "admin/inventory/categories.html",
        form=form,
        page_title="Categories Management",
        table="brands_categories",
        site="Category",
    )


@endpoint.route("/inventory/brands", methods=["GET", "POST"])
def page_table_brands():
    form = AddBrand(request.form)
    """inserting brands"""
    if request.method == "POST" and form.validate():
        brand = Brand(name=form.name.data, desc=form.desc.data)
        db = TableBC()
        db.insert(brand)
        db.close()
    return render_template(
        "admin/inventory/brands.html",
        form=form,
        page_title="Brands Management",
        table="brands_categories",
        site="Brand",
    )


@endpoint.route("/inventory/brands/data_table")
def api_table_brands():
    db = TableBC()
    entries = [i.to_json() for i in db.objects() if i.role == "brand"]
    db.close()
    print("-- Retrieving entries for brands. --")
    return wrappers.Response(
        status=200, content_type="application/json", response=json.dumps(entries)
    )


@endpoint.route("/inventory/categories/data_table")
def api_table_categories():
    db = TableBC()
    entries = [i.to_json() for i in db.objects() if i.role == "cat"]
    db.close()
    print("-- Retrieving entries for categories --")
    return wrappers.Response(
        status=200, content_type="application/json", response=json.dumps(entries)
    )


@endpoint.route("/inventory/add/products", methods=["GET", "POST"])
def page_products_add():
    """
    get brands and categories for the product
    """
    db = TableBC()
    items = db.objects()
    brands = [x for x in items if x.role == "brand"]
    categories = [x for x in items if x.role == "cat"]
    db.close()
    form = AddProduct()

    if request.method == "POST" and form.validate_on_submit():
        print("added")
        product = Product(
            name=form.name.data,
            brand=request.form.get("brand"),
            category=request.form.get("category"),
            centprice=form.centprice.data,
            stock=form.stock.data,
            desc=form.desc.data,
            discount=form.discount.data,
        )
        for x in range(3):
            image_product = Image.open(request.files.get(f"image_{x}"))
            image_product = image_product.resize((600, 600))
            image_product.convert("RGB")
            image_product.save(
                f"{basedir}/static/media/img_products/{product.uuid}_{x}.png"
            )
            product.images = {x: f"img_products/{product.uuid}_{x}.png"}
        db = TableProduct()
        db.insert(product)
        db.close()
        flash(f"{form.name.data} has been added!")
    return render_template(
        "admin/inventory/form_products.html",
        form=form,
        brands=brands,
        categories=categories,
        page_title="Add Products",
    )


@endpoint.route("/inventory")
def page_table_products():
    db_products = TableProduct()
    products = db_products.objects()
    db_bc = TableBC()
    bc = db_bc.dict()
    db_bc.close()
    for x in products:
        try:
            bc[x.brand]
        except:
            x.brand = "0"
            db_products.insert(x)
        try:
            bc[x.cat]
        except:
            x.cat = "1"
            db_products.insert(x)
    db_products.close()
    return render_template(
        "admin/inventory/table_products.html",
        products=products,
        bc=bc,
        page_title="Inventory Management",
    )


@endpoint.route("/inventory/update/<uid>", methods=["GET", "POST"])
def page_update_products(uid):
    form = UpdateProduct()

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

    db_products = TableProduct()
    target = db_products.retrieve(uid)
    db_products.close()

    db_bc = TableBC()
    bc = db_bc.dict()
    db_bc.close()
    brands = [bc[x] for x in bc if bc[x].role == "brand"]
    categories = [bc[x] for x in bc if bc[x].role == "cat"]

    if request.method == "POST" and form.validate_on_submit():
        db = TableProduct()
        attributes = {
            "name": form.name.data,
            "brand": request.form.get("brand"),
            "cat": request.form.get("category"),
            "centprice": form.centprice.data,
            "stock": form.stock.data,
            "desc": form.desc.data,
            "discount": form.discount.data,
        }
        images = {
            0: request.files.get("image_0"),
            1: request.files.get("image_1"),
            2: request.files.get("image_2"),
        }

        """
        checks if form field is blank
        replaces original if isnt
        """
        for key, value in attributes.items():
            if check_valid(value):
                setattr(target, key, value)

        """
        checks if images field is blank
        replaces original if isnt
        """
        for x in images:
            if images[x].filename.replace(" ", "") != "":
                image_product = Image.open(images[x])
                image_product = image_product.resize((600, 600))
                image_product.convert("RGB")
                image_product.save(
                    f"{basedir}/static/media/img_products/{target.uuid}_{x}.png"
                )
                target.images = {x: f"img_products/{target.uuid}_{x}.png"}
                print("Replaced Completed")

        db.insert(target)
        db.close()
    return render_template(
        "admin/inventory/update/products.html",
        form=form,
        target=target,
        bc=bc,
        brands=brands,
        categories=categories,
    )
