import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

project_id = "madereria"
credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

def get_users():
    return db.collection('users').get()

def get_user(user_id):
    return db.collection('users').document(user_id).get()

def user_put(user_data):
    user_ref = db.collection('users').document(user_data.username)
    user_ref.set({'password': user_data.password, 'admin': user_data.is_admin})

def get_products():
    return db.collection('producto').get()

def get_product(product_id):
    return db.collection('producto').document(product_id).get()

def product_put(producto, precio):
    todos_collection_ref = db.collection('producto').document(producto)
    todos_collection_ref.set({'precio': precio})

def item_cart_put(user_id, product_id, precio, cantidad):
    cart_collection_ref = db.collection('cart').document(user_id).collection('product_id').document(product_id)
    cart_collection_ref.set({'precio': precio, 'cantidad': cantidad})

def get_cart_items(user_id):
    return db.collection('cart').document(user_id).collection('product_id').get()

def get_cart_item(user_id, product_id):
    return db.collection('cart').document(user_id).collection('product_id').document(product_id).get()

def delete_item(user_id, product_id):
    item_ref = item_get_ref(user_id, product_id)
    item_ref.delete()

def reg_sell(user_id, id, product_id, precio, precio_total):
    todos_collection_ref = db.collection('ventas').document(user_id).collection(id)
    todos_collection_ref.set({'producto': product_id, 'precio': precio, 'precio_total': precio_total})

def delete_product(product_id):
    product_ref = product_get_ref(product_id)
    product_ref.delete()

def update_product(product_id, product_id_n, precio_n):
    product_ref = product_get_ref(product_id)
    product_ref.update({ 'producto': product_id_n, 'precio': precio_n })

def product_get_ref(product_id):
    return db.document('producto/{}'.format(product_id))

def item_get_ref(user_id, product_id):
    return db.document('cart/{}/product_id/{}'.format(user_id, product_id))




def get_todos(user_id):
    return db.collection('users').document(user_id).collection('todos').get()

def put_todo(user_id, descripcion):
    todos_collection_ref = db.collection('users').document(user_id).collection('todos')
    todos_collection_ref.add({'descripcion': descripcion, 'done': False})

def delete_todo(user_id, todo_id):
    todo_ref = todo_get_ref(user_id, todo_id)
    todo_ref.delete()

def update_todo(user_id, todo_id, done):
    todo_done = not bool(done)
    todo_ref = todo_get_ref(user_id, todo_id)
    todo_ref.update({'done': todo_done})

def todo_get_ref(user_id, todo_id):
    return db.document('users/{}/todos/{}'.format(user_id, todo_id))
