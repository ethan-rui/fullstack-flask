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
    # cant put int:param in url
    try:
        no_pg = int(request.args.get("page"))
        size_pg = int(request.args.get("size"))
        param_filter = request.args.get("filter_by")
        param_sort = request.args.get("sort_by")
    except:
        no_pg = 0
        size_pg = 1
        param_filter = None
        param_sort = None

    db_products = TableProduct()
    products = db_products.objects()
    db_bc = TableBC()
    bc = db_bc.dict()
    db_bc.close()
    db_products.close()
    shown_products = products[(no_pg * size_pg) : (no_pg * size_pg + size_pg)]
    total_pg = ceil(len(products) / size_pg)
    return render_template("common/catalog.html", shown_products=shown_products, bc=bc)


@endpoint.route("/info_product/<uid>")
def page_info_product(uid):
    db_products = TableProduct()
    products = db_products.retrieve(uid)
    db_products.close()
    return render_template("common/info_product.html", products=products)


@endpoint.route("/inquiry/", methods=["GET", "POST"])
def page_inquiry():
    form = InquiryForm(request.form)
    if form.validate() and request.method == "POST":
        print("---hello__")
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