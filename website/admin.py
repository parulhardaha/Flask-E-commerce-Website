from flask import Blueprint, render_template,flash, redirect, url_for,send_from_directory
from flask_login import login_required, current_user
from .forms import ShopItemsForm
from werkzeug.utils import secure_filename
from .models import Product
from . import db
from website import db

admin=Blueprint('admin', __name__)

@admin .route('/media/<path:filename>') #<path:filename> pick filename from url
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id == 1:  # Admin
        form = ShopItemsForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data
            file_name = secure_filename(file.filename)  
            file_path = f'./media/{file_name}'
            file.save(file_path)

            new_item = Product(
                product_name=product_name,
                current_price=current_price,
                previous_price=previous_price,
                in_stock=in_stock,
                flash_sale=flash_sale,
                product_picture=file_path
            )

            try:
                db.session.add(new_item)
                db.session.commit()
                print(f"Item added: {new_item}")  # Debug print
                flash(f'{product_name} added Successfully')
                return redirect(url_for('admin.add_shop_items'))
            except Exception as e:
                print(f"Error: {e}")  # Debug print
                db.session.rollback()
                flash('The item has not been added')

        return render_template('add-shop-items.html', form=form)
    else:
        return render_template('404.html')


@admin.route('/shop_items', methods=['GET', 'POST'])
@login_required
def shop_items():
    print(f"Current User ID: {current_user.id}")  # Debug print
    if current_user.id == 1:
        items = Product.query.all()  #list of all items
        print(f"Fetched {len(items)} products")  # Debug print
        return render_template('shop_items.html', items=items)
    else:
        return render_template('404.html')




      
