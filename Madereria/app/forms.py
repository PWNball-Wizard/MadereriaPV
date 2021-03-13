from itertools import product
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DecimalField

class LoginForm(FlaskForm):#extiende a flask form herencia
    username = StringField('Nombre de usuario', validators =[DataRequired()])
    password = PasswordField('Password', validators =[DataRequired()])
    submit = SubmitField('Enviar')

class ProductForm(FlaskForm):
    product = StringField('Producto', validators=[DataRequired()])
    price = StringField('Precio', validators = [DataRequired()])
    submit = SubmitField('Crear')

class SignupForm(FlaskForm):
    username = StringField('Nombre de usuario', validators =[DataRequired()])
    password = PasswordField('Password', validators =[DataRequired()])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Enviar')

class AddCart(FlaskForm):
    quantity = StringField('Cantidad', validators = [DataRequired()])
    submit = SubmitField('Agregar al Carrito')

class DeleteCart(FlaskForm):
    submit = SubmitField('Eliminar')

class RegisterSell(FlaskForm):
    submit = SubmitField('Registrar Venta')

class DeleteInv(FlaskForm):
    submit = SubmitField('Eliminar')

class UpdateInv(FlaskForm):
    producto = StringField('Producto', validators = [DataRequired()])
    precio = StringField('Precio', validators = [DataRequired()])
    submit = SubmitField('Actualizar')

class TodoForm(FlaskForm):
    description = StringField('Descripcion',  validators =[DataRequired()])
    submit = SubmitField('Crear')

class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')

class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')

