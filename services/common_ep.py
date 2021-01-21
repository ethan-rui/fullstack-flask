from flask import render_template, redirect, url_for, Blueprint, request, flash
from data.user_pages import TableUserPages
from data.products import TableBC, TableProduct
from data.inquiries import TableInquiry, Inquiry
from math import ceil
from services.forms.inquiry import InquiryForm

endpoint = Blueprint("base", __name__)


@endpoint.route("/")
def page_home():
    # featured products -> uuid of products
    db_featured = TableUserPages()
    promo_products = db_featured.dict()["promo_products"]
    db_featured.close()

    # existing products
    db_products = TableProduct()
    promo_products_data = [db_products.dict()[i] for i in promo_products]
    db_products.close()

    # uuid to crossreference the product
    db_bc = TableBC()
    brands = [x for x in db_bc.objects() if x.role == "brand"]
    categories = [x for x in db_bc.objects() if x.role == "category"]
    db_bc.close()

    return render_template(
        "common/home.html", products=promo_products_data, cats=categories, brands=brands
    )


@endpoint.route("/catalog/")
def page_catalog():
    """pg_index starts from 0"""
    pg_index = request.args.get("page", type=int, default=0)
    pg_size = request.args.get("size", type=int, default=10)
    param_filter = request.args.get("filter_by", type=str, default=None)
    param_sort = request.args.get("sort_by", type=str, default="popularity")

    db_products = TableProduct()
    products = db_products.objects()
    db_bc = TableBC()
    bc = db_bc.dict()
    db_bc.close()
    db_products.close()

    shown_products = products[(pg_index * pg_size) : (pg_index * pg_size + pg_size)]
    pg_total = ceil(len(products) / pg_size)
    return render_template(
        "common/catalog.html",
        shown_products=shown_products,
        bc=bc,
        pg_total=pg_total,
        param_filter=param_filter,
        param_sort=param_sort,
        pg_index=pg_index,
        pg_size=pg_size,
    )


@endpoint.route("/catalog/product/<uid>")
def page_info_product(uid):
    db_products = TableProduct()
    target = db_products.retrieve(uid)
    db_products.close()
    return render_template("common/info_product.html", target=target)


@endpoint.route("/inquiry", methods=["GET", "POST"])
def page_inquiry():
    form = InquiryForm(request.form)
    if request.method == "POST" and form.validate():
        db = TableInquiry()
        inquiry = Inquiry(
            sender_name=form.sender_name.data,
            sender_email=form.sender_email.data,
            subject=form.subject.data,
            content=form.content.data,
        )
        db.insert(inquiry)
        flash("Your inquiry has been submitted!")
        db.close()
        return redirect(url_for("base.page_home"))
    return render_template("common/inquiry.html", form=form)