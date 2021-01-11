from flask import render_template, redirect, request, Blueprint, session, url_for, flash
from flask_login.utils import login_required, current_user
from flask_uploads import UploadSet, IMAGES
from data.products import Product, TableProduct, Brand, Category, TableBC
from data import Database
from ..forms.inventory import AddProduct, AddBrand, AddCategory, UpdateProduct
import os

endpoint = Blueprint("admin_inventory", __name__)
photos = UploadSet("photos", IMAGES)
basedir = os.getcwd()


@endpoint.before_request
@login_required
def check_perms():
    from .common_api import authorizer

    return authorizer(current_user)


@endpoint.route("/inventory/<site>/update/<uid>", methods=["POST"])
def page_update_bc(uid, site):
    if request.method == "POST":
        db = TableBC()
        target = db.retrieve(uid)
        target.name = request.form["name"]
        target.desc = request.form["desc"]
        db.insert(target)
        db.close()
        print("Updated successful!")
        if site.lower() in ["categories", "category"]:
            return redirect(url_for("admin_inventory.page_table_categories"))
        elif site.lower() in ["brands", "brand"]:
            return redirect(url_for("admin_inventory.page_table_brands"))
        else:
            return redirect(url_for("admin_statistics.page_dashboard"))


@endpoint.route("/inventory/categories", methods=["GET", "POST"])
def page_table_categories():
    form = AddCategory()
    if request.method == "POST" and form.validate_on_submit():
        cat = Category(name=form.name.data, desc=form.desc.data)
        db = TableBC()
        db.insert(cat)
        db.close()
    db = TableBC()
    entries = [x for x in db.objects() if x.role == "cat"]
    db.close()
    return render_template(
        "admin/inventory/categories.html",
        form=form,
        entries=entries,
        page_title="Categories Management",
    )


@endpoint.route("/inventory/brands", methods=["GET", "POST"])
def page_table_brands():
    form = AddBrand(request.form)
    if request.method == "POST" and form.validate():
        brand = Brand(name=form.name.data, desc=form.desc.data)
        db = TableBC()
        db.insert(brand)
        db.close()
    db = TableBC()
    entries = [x for x in db.objects() if x.role == "brand"]
    db.close()
    return render_template(
        "admin/inventory/brands.html",
        form=form,
        entries=entries,
        page_title="Brands Management",
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
            product.images = {
                x: photos.save(
                    request.files.get(f"image_{x}"),
                    folder="img_products",
                    name=f"{product.uuid}_x.",
                )
            }
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

        for key, value in attributes.items():
            if check_valid(value):
                setattr(target, key, value)

        photo_path = f"{basedir}/static/media/img_products/"
        for key, value in images.items():
            if value.filename.strip(" ") != "":
                [
                    os.remove(f"{photo_path}/{x}")
                    for x in os.listdir(photo_path)
                    if x.startswith(f"{target.uuid}_{key}")
                ]
                target.images = {key: value}

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
