from app.models import UserData, UserModel
from app.forms import SignupForm, ProductForm, DeleteInv, UpdateInv
from flask import render_template, redirect, flash, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from . import admin
from app.auth.views import admin_required
from app.firestore_service import get_user, user_put, get_product, get_products, delete_product, update_product, product_put, get_cart_items
from werkzeug.security import generate_password_hash, check_password_hash

@admin.route('signup', methods=['GET', 'POST'])
@login_required
@admin_required
def signup():
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        password = signup_form.password.data
        is_admin = signup_form.is_admin.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash, is_admin)
            user_put(user_data)

            user = UserModel(user_data)
            login_user(user)
            flash('Bienvenido')

            return redirect(url_for('hello'))

        else:
            flash('Usuario existente')

    return render_template('signup.html', **context)

@admin.route('inventario', methods=['GET', 'POST'])
@login_required
@admin_required
def inventario():
    product_form = ProductForm()
    delete_form = DeleteInv()
    update_form = UpdateInv() 

    context = {
        'product_form': product_form,
        'productos' : get_products(),
        'delete_form': delete_form,
        'update_form': update_form,
    }

    if product_form.validate_on_submit():
        nombre = product_form.product.data
        price = product_form.price.data
        user_doc = get_product(nombre)

        if user_doc.to_dict() is None:
            product_put(nombre, price)
            flash('Producto agregado con exito')
            return redirect(url_for('hello'))
        else:
            flash(f'El producto {nombre} ya está en tu inventario')

    return render_template('inventario.html', **context)

@admin.route('/inventario/delete/<product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def inv_eliminar(product_id):
    delete_product(product_id = product_id)
    return redirect(url_for('admin.inventario'))

@admin.route('/inventario/update/<product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def inv_update(product_id):
    update_form = UpdateInv()

    if update_form.validate_on_submit():
        update_product(product_id = product_id, product_id_n = update_form.producto.data, precio_n = update_form.precio.data)
        flash('Producto actualizado con exito')

    return redirect(url_for('admin.inventario'))