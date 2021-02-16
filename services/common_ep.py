from flask import render_template, redirect, url_for, Blueprint, request, flash, escape
from data.products import TableBC, TableProduct
from data.inquiries import TableInquiry, Inquiry
from data.frontpage import TableFrontPage
from math import ceil
from services.forms.inquiry import InquiryForm
from operator import attrgetter

endpoint = Blueprint("base", __name__)


@endpoint.route("/")
def page_home():
    db = TableFrontPage()
    db.close()
    db_bc = TableBC()
    bc = db_bc.dict()
    db_bc.close()
    db_products = TableProduct()
    product_keys = db_products.dict()
    """check the existence of the featured products in dict"""
    featured_products = [x for x in db.table["featured_products"] if x in product_keys]
    """retrieving the carousel images"""
    try:
        carou_active_key = list(db.carousel.keys())[0]
        carou_others_keys = list(db.carousel.keys())[1:]
    except IndexError:
        carou_active_key = ""
        carou_others_keys = ""
    """wont render if carousel is empty"""

    return render_template(
        "common/home.html",
        img_carousel=db.carousel,
        carou_active_key=carou_active_key,
        carou_others_keys=carou_others_keys,
        featured_products=featured_products,
        product_keys=product_keys,
        bc=bc,
    )


@endpoint.route("/catalog/")
def page_catalog():
    """pg_index starts from 0"""
    pg_index = request.args.get("page", type=int, default=0)
    pg_size = request.args.get("size", type=int, default=10)
    param_filter_brands = request.args.get("filter_by_brand", type=str, default="")
    param_filter_categories = request.args.get("filter_by_cat", type=str, default="")
    param_sort = request.args.get("sort_by", type=str, default="price_asc")
    param_search = request.args.get("search", type=str, default="").replace("-", " ")

    db_products = TableProduct()
    """querying the object based on search params"""
    if param_search != "":
        products_by_name = db_products.query({"name": param_search}, mode="similar")
    else:
        products_by_name = db_products.objects()

    """param filters -> list of uuid """
    if param_filter_brands != "":
        filtered_brands = list(param_filter_brands.split(","))
        print(param_filter_brands)
        products_by_brand = [i for i in products_by_name if i.brand in filtered_brands]
    else:
        products_by_brand = []

    if param_filter_categories != "":
        filtered_categories = list(param_filter_categories.split(","))
        products_by_cat = [i for i in products_by_name if i.cat in filtered_categories]
    else:
        products_by_cat = []

    """all the products -> set"""
    """no duplicates in set"""

    products = list(set(products_by_name + products_by_brand + products_by_cat))

    """removed all low stocks"""
    products = [x for x in products if x.stock > 0]

    """sorting the products based on sorting params"""
    if param_sort != "":
        if param_sort == "price_asc":
            products = sorted(
                products, key=attrgetter("centprice_final"), reverse=False
            )
        if param_sort == "price_desc":
            products = sorted(products, key=attrgetter("centprice_final"), reverse=True)
        if param_sort == "popularity":
            products = sorted(products, key=attrgetter("quantity_sold"), reverse=True)

    """gets the respective brands and cat for each product"""
    db_bc = TableBC()
    bc = db_bc.dict()
    db_bc.close()
    db_products.close()

    if pg_size <= 0:
        pg_size = 1
    pg_total = ceil(len(products) / pg_size)
    if pg_index > pg_total or pg_index < 0:
        pg_index = 0

    shown_products = products[(pg_index * pg_size) : (pg_index * pg_size + pg_size)]
    len_products = len(products)
    return render_template(
        "common/catalog.html",
        shown_products=shown_products,
        bc=bc,
        pg_total=pg_total,
        param_filter_brands=param_filter_brands,
        param_filter_categories=param_filter_categories,
        param_sort=param_sort,
        param_search=param_search,
        pg_index=pg_index,
        pg_size=pg_size,
        len_products=len_products,
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
            content=escape(form.content.data),
            status=True,
        )
        db.insert(inquiry)
        flash("Your inquiry has been submitted!")
        db.close()
        return redirect(url_for("base.page_home"))
    return render_template("common/inquiry.html", form=form)