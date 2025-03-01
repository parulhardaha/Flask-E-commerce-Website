from flask import Blueprint, render_template,flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import ShopItemsForm
from werkzeug.utils import secure_filename
from .models import Product
from . import db

admin=Blueprint('admin', __name__)

@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.id==1:  #admin
        form = ShopItemsForm()
        #data for post request
        if form.validate_on_submit():
            product_name=form.product_name.data
            current_price=form.current_price.data
            previous_price=form.previous_price.data
            in_stock=form.in_stock.data
            flash_sale=form.flash_sale.data

            file=form.product_picture.data
            file_name=secure_filename(file.filename) # remove whitespaces and special chars to _
            #media dictrectory to store file(product pics)
            file_path=f'./media/{file_name}'
            file.save(file_path)

            new_item=Product()
            new_item.product_name=product_name
            new_item.current_price=current_price
            new_item.previous_price=previous_price
            new_item.in_stock=in_stock
            new_item.flash_sale=flash_sale

            new_item.product_picture=file_path #/media/lipstick

            #add produts to db
            try:
                db.session.add(new_item)
                db.session.commit()
                #flash(f'{product_name} added Successfully')
                #return render_template('add-shop-items.html', form=form)
                flash(f'{product_name} added Successfully')
                return redirect(url_for('admin.add_shop_items'))
            except Exception as e:
                print(e)
                db.session.rollback() 
                flash('The item has not been added')





        
        
        
        return render_template('add-shop-items.html',form=form)
    else:
        return render_template('404.html')
