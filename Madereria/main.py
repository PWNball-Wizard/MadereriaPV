import unittest
from flask import request, make_response, redirect, session, url_for, flash, jsonify
from flask.templating import render_template
from flask_login import login_required, current_user
from app import create_app
from app.firestore_service import get_users, get_cart_items, get_cart_item, delete_item, get_product, get_products, item_cart_put, reg_sell, delete_todo, update_todo
from app.forms import AddCart, DeleteTodoForm, UpdateTodoForm, DeleteCart, RegisterSell

app = create_app()

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)

@app.errorhandler(400)
def not_found(error):
    return render_template('404.html', error = error)

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error = error)

@app.route("/")
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip
    return response

@app.route('/carrito/add/<product_id>', methods = ['GET','POST'])
@login_required
def add_to_cart(product_id):
    add_to_cart_form = AddCart()
    usuario = current_user.id
    producto = get_product(product_id = product_id)
    precio = producto.to_dict()['precio']
    if add_to_cart_form.validate_on_submit:
        verifica_producto = get_cart_item(user_id = usuario, product_id = product_id)
        if verifica_producto.to_dict() is None:
            item_cart_put(user_id = usuario, product_id = producto.id, precio = precio, cantidad = add_to_cart_form.quantity.data)
            flash('Producto agregado al carrito de compra')
        else:
            flash(f'El producto {product_id} ya esta en el carrito de compra, prueba actualizar')
    return redirect(url_for('hello'))

@app.route('/carrito/delete/<product_id>', methods = ['GET','POST'])
@login_required
def del_from_cart(product_id):
    usuario = current_user.id

    delete_item(user_id = usuario, product_id = product_id)

    return redirect(url_for('hello'))

@app.route('/carrito/registrar/', methods = ['GET','POST'])
@login_required
def reg_sell():
    reg_venta = RegisterSell()
    usuario = current_user.id
    productos = get_cart_items(user_id = usuario)
    if reg_venta.validate_on_submit:
        precio_total = 0
        if productos.to_dict() is not None:
            for producto in productos:
                precio_total += (float(producto.to_dict()['precio']) * int(producto.to_dict()['cantidad']))
                reg_sell(user_id = usuario, product_id = producto.id, precio = producto.to_dict()['precio'])
                flash('Venta registrada con exito')
    return redirect(url_for('hello'))

@app.route("/hello", methods = ['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    add_cart_form = AddCart()
    delete_cart_form = DeleteCart()
    carrito = get_cart_items(user_id = current_user.id)

    precio_total = 0
    for item in carrito:
        precio_total += (float(item.to_dict()['precio']) * int(item.to_dict()['cantidad']))

    context = {'user_ip' : user_ip,
                'productos' : get_products(),
                'carrito_compra' : carrito,
                'username': username,
                'add_cart_form': add_cart_form,
                'precio_total': precio_total,
                'delete_cart_form': delete_cart_form,
                }
    if False:
        pass
        flash('Tarea registrada con exito')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)#(**context) es como si pasaramos una a una las variables una por una en automatico

@app.route('/todos/delete/<todo_id>', methods = ['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id = user_id, todo_id = todo_id)

    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods = ['POST'])
def update(todo_id, done):
    user_id = current_user.id
    print('DONE', done)
    update_todo(user_id = user_id, todo_id = todo_id, done = done)

    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.run(debug= False)#Para inicializar el debug es debug = True o 1, sirve para no tener que apagar y prender el server