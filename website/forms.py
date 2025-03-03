from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileRequired

class SignUpForm(FlaskForm):
    email=EmailField('Email', validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired(), Length(min=2)])
    password1=PasswordField('Enter Your Password', validators=[DataRequired(),Length(min=6)])
    password2=PasswordField('Confirm Your Password', validators=[DataRequired(),Length(min=6)])
    submit=SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email=EmailField('Email', validators=[DataRequired()])
    password=PasswordField('Enter Your Password', validators=[DataRequired(),Length(min=6)]) 
    submit=SubmitField('Log in')

class PasswordChangeForm(FlaskForm):
    current_password=PasswordField('Current Password', validators=[DataRequired(),Length(min=6)])   
    new_password=PasswordField('New Password', validators=[DataRequired(),Length(min=6)])
    confirm_new_password=PasswordField('Confirm New Password', validators=[DataRequired(),Length(min=6)])
    submit=SubmitField('Change Password')

class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Picture', validators=[FileRequired()])
    flash_sale = BooleanField('Flash Sale')

    # Buttons
    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update Product')

    def set_placeholders(self, item):
        """Set dynamic placeholders"""
        self.product_name.render_kw = {"placeholder": item.product_name}
        self.previous_price.render_kw = {"placeholder": item.previous_price}
        self.current_price.render_kw = {"placeholder": item.current_price}
        self.in_stock.render_kw = {"placeholder": item.in_stock}
        self.flash_sale.render_kw = {"placeholder": str(item.flash_sale)}
