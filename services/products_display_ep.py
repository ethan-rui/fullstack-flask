#This is a direct copy from the indian tutorial guy. I will modify an fix it to the correct naming conventions later. ~Jin Rong 
from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets, os

@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    brands= Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all
    return render_template('products/single_page.html', product=product, brands=brands, categories=categories)

@app.route('/brand/<int:id>')
def get_brand(id):
    get_b=Brand.query.filter_by(id=id).first_or_404()
    page = request.args.get('page', 1, type=int)
    brand = Addproduct.query,filter_by(brand=get_b).paginate(page=page, per_page=6)
    brands= Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all
    return render_template('products/index.html', brand=brand, brands=brands, categories=categories, get_b=get_b)

@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page', 1, type=int)
    get_cat=Category.query.filter_by(id=id).first_or_404()
    brands= Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=6)
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all
    return render_template('products/index.html', get_cat_prod=get_cat_prod, categories=categories, brands=brands, get_cat=get_cat)
