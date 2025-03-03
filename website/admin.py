from flask import Blueprint, render_template,flash, redirect, url_for,send_from_directory
from flask_login import login_required, current_user
from .forms import ShopItemsForm
from werkzeug.utils import secure_filename
from .models import Product
from . import db
from website import db

admin=Blueprint('admin', __name__)

@admin .route('/media/<path:filename>') #<path:filename> pick filename from url(dynamic)
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

@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    print(f"Item ID --> {item_id}")  # Debugging

    if current_user.id == 1:
        item_to_update = Product.query.get(item_id)
        if not item_to_update:
            flash("Item not found!", "danger")
            return redirect(url_for('admin.shop_items'))

        form = ShopItemsForm(obj=item_to_update)  #fetch with existing data

        #replace with updated values
        if form.validate_on_submit():
            item_to_update.product_name = form.product_name.data
            item_to_update.previous_price = form.previous_price.data
            item_to_update.current_price = form.current_price.data
            item_to_update.in_stock = form.in_stock.data
            item_to_update.flash_sale = form.flash_sale.data

            if form.product_picture.data:
                file = form.product_picture.data
                file_name = secure_filename(file.filename)
                file_path = f'./media/{file_name}'
                file.save(file_path)
                item_to_update.product_picture = file_path

            try:
                db.session.commit()
                flash("Item updated successfully!", "success")
                return redirect(url_for('admin.shop_items')) 
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating item: {e}", "danger")

        return render_template('update-item.html', form=form, item=item_to_update) 
    else:
        return render_template('404.html')
