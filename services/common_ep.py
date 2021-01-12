from flask import render_template, redirect, url_for, Blueprint, request
from data.user_pages import TableUserPages
from data.products import TableBC, TableProduct
from data.inquiries import TableInquiry
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


@endpoint.route("/products")
def page_display_products():
    db_products = TableProduct()
    products = db_products.objects()
    db_bc = TableBC()
    bc = db_bc.dict()
    db_bc.close()
    db_products.close()
    return render_template("common/display_products.html", products=products, bc=bc)


@endpoint.route("/info_product/<uid>")
def page_info_product(uid):
    db_products = TableProduct()
    products = db_products.retrieve(uid)
    db_products.close()
    return render_template("common/info_product.html", products=products)


@endpoint.route("/inquiry/", methods=["GET", "POST"])
def page_inquiry():
    inquiry = InquiryForm(request.form)
    if inquiry.validate():
        db = TableInquiry()
        inquiry = Inquiry(
            name=inquiry.name.data,
            email=inquiry.email.data,
            subject=inquiry.subject.data,
            msg=inquiry.msg.data,
        )
        db.insert(inquiry)
        db.close()
        flash("Your inquiry has been submitted!")
        return redirect(url_for("base.page_home"))
        db.close()
    return render_template("common/inquiry.html", inquiry=inquiry)