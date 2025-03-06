from flask import Blueprint, render_template, flash, redirect, request, jsonify
from .models import Product, Cart, Order
from flask_login import login_required, current_user
from . import db
from intasend import APIService


views=Blueprint('views', __name__)

#place odrer API
API_PUBLISH_KEY= 'ISPubKey_test_7b41d97b-2478-4c1d-8f41-c36a5a3a870b'
API_TOKEN='ISSecretKey_test_78f801c5-6015-473d-8fa7-dfca459c2cee'



@views.route('/')
def home():
    items=Product.query.filter_by(flash_sale=True)
    return render_template('home.html', items=items, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])


@views.route('/add-to-cart/<int:item_id>')
@login_required
def add_to_cart(item_id):
    item_to_add=Product.query.get(item_id)
    item_exists=Cart.query.filter_by(product_link=item_id,customer_link=current_user.id).first()
    if item_exists: #item is already in cart
        try:
            item_exists.qunatity=item_exists.quantiy+1
            db.session.commit()
            flash(f'Quantity of {item_exists.product.product_name} has been updated')
            return redirect(request.referrer)
        except Exception as e:
            print('Quantity not updated', e)
            flash(f'(Quantity of {item_exists.product.product_name} not updated')
            return redirect(request.referrer)
        
    #item does not present in cart-create new instance
    new_cart_item=Cart()
    new_cart_item.quantity=1
    new_cart_item.product_link=item_to_add.id
    new_cart_item.customer_link=current_user.id

    try:
        db.session.add(new_cart_item)
        db.session.commit()
        flash(f'{new_cart_item.product.product_name} added to cart')
    except Exception as e:
        print('Item not added to cart', e)
        flash(f'{new_cart_item.product.product_name} has not been added to Cart')

    return redirect(request.referrer)    

@views.route('/cart')
@login_required
def show_cart():
    cart=Cart.query.filter_by(customer_link=current_user.id).all()
    amount=0
    for item in cart:
        amount+=item.product.current_price*item.quantity

    return render_template('cart.html',cart=cart,amount=amount,total=amount+100)    


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method=='GET':
        cart_id=request.args.get('cart_id')
        
        #increase val
        # Fetch cart item from database
        cart_item = Cart.query.get(cart_id)
        if cart_item:
            cart_item.quantity += 1  #increase quantity
            db.session.commit() 

        # Fetch updated cart data
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)
        

        #sendding updated response to frontend
        data={
                'quantity': cart_item.quantity,
                'amount' : amount,
                'total': amount+100
            }
        
        return jsonify(data)

@views.route('/minuscart')
@login_required
def minus_cart():
    if request.method=='GET':
        cart_id=request.args.get('cart_id')
        
        #increase val
        # Fetch cart item from database
        cart_item = Cart.query.get(cart_id)
        if cart_item:
            cart_item.quantity -= 1  #decrease quantity
            db.session.commit() 

        # Fetch updated cart data
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)
        

        #sendding updated response to frontend
        data={
                'quantity': cart_item.quantity,
                'amount' : amount,
                'total': amount+100
            }
        
        return jsonify(data)        
    

@views.route('/removecart')
@login_required
def remove_cart():
    if request.method=='GET':
        cart_id = request.args.get('cart_id')
        cart_item   = Cart.query.get(cart_id)
        db.session.delete(cart_item)
        db.session.commit()

        # Fetch updated cart data
        cart = Cart.query.filter_by(customer_link=current_user.id).all()
        amount = sum(item.product.current_price * item.quantity for item in cart)
        

        #sendding updated response to frontend
        data={
                'quantity': cart_item.quantity,
                'amount' : amount,
                'total': amount+100
            }
        
        return jsonify(data)    


@views.route('/place_order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link=current_user.id).all()
    
    if not customer_cart:
        flash("Your Cart is Empty")
        return redirect('/')

    try:
        #taking order placement
        for item in customer_cart:
            new_order = Order()
            new_order.quantity = item.quantity
            new_order.price = item.product.current_price
            new_order.status = "Confirmed"  # Fake status
            new_order.product_link = item.product_link
            new_order.customer_link = item.customer_link

            db.session.add(new_order)

            # Reduce stock
            product = Product.query.get(item.product_link)
            product.in_stock -= item.quantity

            # Remove from cart
            db.session.delete(item)

        db.session.commit()
        return render_template("order_confirmation.html")

    except Exception as e:
        print("Order Error:", e)
        flash(f"Order not Placed: {e}")
        return redirect('/')

#view list of orders
@views.route('/orders')
@login_required
def order():
    orders=Order.query.filter_by(customer_link=current_user.id)
    return render_template('orders.html', orders=orders)

@views.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '')  # Get the search query from URL parameters
    
    if search_query:  # If search_query is not empty
        items = Product.query.filter(Product.product_name.ilike(f'%{search_query}%')).all()
    else:
        items = [] 
    
    cart_items = Cart.query.filter_by(customer_link=current_user.id).all() if current_user.is_authenticated else []

    return render_template('search.html', items=items, cart=cart_items)
    


@views.route('/about')
def about():
    return render_template('/about.html')
    