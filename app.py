from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'zingthings_super_secret_key_2024'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'zing@admin123'

# Real toy photos from Unsplash (free to use)
products = [
    {'id': 1,  'name': 'Cosmic Fidget Cube',     'price': 12.99, 'category': 'Fidgets',  'stock': 45, 'emoji': '🎲',
     'img': '/static/images/products/fidget_cube.jpg',
     'desc': 'Satisfying 6-sided fidget cube with buttons, switches, dials and joystick.'},



    {'id': 3,  'name': 'Glow Spinner Pro',         'price': 15.99, 'category': 'Spinners', 'stock': 20, 'emoji': '✨',
     'img': '/static/images/products/spinner.jpg',
     'desc': 'LED light-up spinner with 3 modes. Spins for up to 5 minutes straight!'},

    {'id': 4,  'name': 'Magnetic Putty Ball',      'price': 9.99,  'category': 'Putty',    'stock': 60, 'emoji': '🧲',
     'img': '/static/images/products/putty.jpg',
     'desc': 'Mesmerizing magnetic putty that stretches, bounces and absorbs magnets.'},

    {'id': 5,  'name': 'Pop It Galaxy',            'price': 6.99,  'category': 'Pop-It',   'stock': 80, 'emoji': '💫',
     'img': '/static/images/products/popit.jpg',
     'desc': 'Galaxy-themed pop-it with 60 bubbles. The ultimate stress buster!'},

    {'id': 6,  'name': 'Mini Drone Toy',           'price': 24.99, 'category': 'Tech',     'stock': 15, 'emoji': '🚁',
     'img': '/static/images/products/drone.jpg',
     'desc': 'Palm-sized indoor drone with gyro stabilization. Flips, hovers and races!'},

    {'id': 7,  'name': 'Slime Factory Kit',        'price': 18.99, 'category': 'Slime',    'stock': 35, 'emoji': '🟢',
     'img': '/static/images/products/slime.jpg',
     'desc': 'DIY slime-making kit with 12 colors, glitter, foam beads & more!'},

    {'id': 9,  'name': 'RC Monster Truck',         'price': 34.99, 'category': 'RC Cars',  'stock': 25, 'emoji': '🚗',
     'img': '/static/images/products/rc_truck.jpg',
     'desc': '4WD off-road remote control truck with 2.4GHz control up to 50m range.'},

    {'id': 10, 'name': 'Kinetic Sand Set',         'price': 14.99, 'category': 'Sand',     'stock': 40, 'emoji': '🏖️',
     'img': '/static/images/products/kinetic_sand.jpg',
     'desc': '2kg magical kinetic sand that never dries out, with molds and tools.'},

    {'id': 11, 'name': 'LEGO Classic Bricks',      'price': 29.99, 'category': 'Building', 'stock': 55, 'emoji': '🧱',
     'img': '/static/images/products/lego.jpg',
     'desc': '900-piece classic brick set with 33 colors. Build anything you imagine!'},

    {'id': 12, 'name': "Rubik's Speed Cube",       'price': 11.99, 'category': 'Puzzles',  'stock': 38, 'emoji': '🟥',
     'img': '/static/images/products/rubiks.jpg',
     'desc': 'Competition-grade 3x3 speed cube with corner cutting & smooth turns.'},

    {'id': 13, 'name': 'Magnetic Tile Set',        'price': 39.99, 'category': 'Building', 'stock': 22, 'emoji': '🔷',
     'img': '/static/images/products/magnetic_tiles.jpg',
     'desc': '60-piece magnetic construction tiles. Build 2D and 3D structures!'},

    {'id': 15, 'name': 'Foam Nerf Blaster',        'price': 19.99, 'category': 'Outdoor',  'stock': 30, 'emoji': '🔫',
     'img': '/static/images/products/nerf.jpg',
     'desc': 'Motorized foam blaster with 20-dart drum. Auto-fire mode included!'},

    {'id': 16, 'name': 'Science Experiment Kit',   'price': 22.99, 'category': 'Science',  'stock': 28, 'emoji': '🔬',
     'img': '/static/images/products/science_kit.jpg',
     'desc': '30+ experiments: volcanoes, crystals, slime, invisible ink & more!'},
]
feedbacks = [
    {'name': 'Priya S.', 'rating': 5, 'comment': 'My kids LOVE the Pop It Galaxy! Keeps them busy for hours. Delivery was super fast too. 🌟', 'product': 'Pop It Galaxy'},
    {'name': 'Rahul M.', 'rating': 5, 'comment': 'The RC Monster Truck is incredible quality for the price. My son hasn\'t put it down since it arrived!', 'product': 'RC Monster Truck'},
    {'name': 'Ananya K.', 'rating': 4, 'comment': 'Slime Factory Kit was a big hit at my daughter\'s birthday party. Super fun and easy to follow instructions.', 'product': 'Slime Factory Kit'},
    {'name': 'Dev P.',   'rating': 5, 'comment': 'Ordered the Science Kit and it arrived next day. The experiments are genuinely educational and fun!', 'product': 'Science Experiment Kit'},
    {'name': 'Meera T.', 'rating': 5, 'comment': 'ZingThings is our go-to toy shop. Best prices, fast shipping, and always great quality. Highly recommend! ⚡', 'product': 'Cosmic Fidget Cube'},
]

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login to access the admin panel.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ===================== PUBLIC ROUTES =====================

@app.route('/')
def index():
    return render_template('index.html', products=products, feedbacks=feedbacks)

@app.route('/shop')
def shop():
    category = request.args.get('category', 'All')
    categories = ['All'] + sorted(list(set(p['category'] for p in products)))
    filtered = products if category == 'All' else [p for p in products if p['category'] == category]
    return render_template('shop.html', products=filtered, categories=categories, active=category)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart_items.items():
        p = next((x for x in products if x['id'] == int(pid)), None)
        if p:
            subtotal = p['price'] * qty
            total += subtotal
            items.append({**p, 'qty': qty, 'subtotal': subtotal})
    return render_template('cart.html', items=items, total=round(total, 2))

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', {})
    items = []
    total = 0
    for pid, qty in cart_items.items():
        p = next((x for x in products if x['id'] == int(pid)), None)
        if p:
            subtotal = p['price'] * qty
            total += subtotal
            items.append({**p, 'qty': qty, 'subtotal': subtotal})
    if not items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('shop'))
    return render_template('checkout.html', items=items, total=round(total, 2))

@app.route('/order-success')
def order_success():
    order_id = session.pop('order_id', 'ZT-0000')
    session.pop('cart', None)
    return render_template('order_success.html', order_id=order_id)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        rating = int(request.form.get('rating', 5))
        comment = request.form.get('comment', '').strip()
        product_name = request.form.get('product', '').strip()
        if name and comment:
            feedbacks.insert(0, {'name': name, 'rating': rating, 'comment': comment, 'product': product_name})
            flash('Thanks for your feedback! 🎉', 'success')
        return redirect(url_for('feedback'))
    return render_template('feedback.html', feedbacks=feedbacks, products=products)

# ===================== CART API ROUTES =====================

@app.route('/api/cart/add', methods=['POST'])
def api_cart_add():
    data = request.get_json()
    pid = str(data.get('id'))
    cart = session.get('cart', {})
    cart[pid] = cart.get(pid, 0) + 1
    session['cart'] = cart
    session.modified = True
    count = sum(cart.values())
    return jsonify({'success': True, 'count': count})

@app.route('/api/cart/update', methods=['POST'])
def api_cart_update():
    data = request.get_json()
    pid = str(data.get('id'))
    qty = int(data.get('qty', 1))
    cart = session.get('cart', {})
    if qty <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = qty
    session['cart'] = cart
    session.modified = True
    count = sum(cart.values())
    return jsonify({'success': True, 'count': count})

@app.route('/api/cart/remove', methods=['POST'])
def api_cart_remove():
    data = request.get_json()
    pid = str(data.get('id'))
    cart = session.get('cart', {})
    cart.pop(pid, None)
    session['cart'] = cart
    session.modified = True
    count = sum(cart.values())
    return jsonify({'success': True, 'count': count})

@app.route('/api/cart/count')
def api_cart_count():
    cart = session.get('cart', {})
    return jsonify({'count': sum(cart.values())})

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    import random, string
    order_id = 'ZT-' + ''.join(random.choices(string.digits, k=6))
    session['order_id'] = order_id
    return jsonify({'success': True, 'order_id': order_id, 'redirect': url_for('order_success')})

# ===================== ADMIN ROUTES =====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session['admin_user'] = username
            flash('Welcome back, Admin! 🎉', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_products = len(products)
    total_stock = sum(p['stock'] for p in products)
    categories = len(set(p['category'] for p in products))
    total_value = sum(p['price'] * p['stock'] for p in products)
    stats = {
        'total_products': total_products,
        'total_stock': total_stock,
        'categories': categories,
        'total_value': round(total_value, 2),
    }
    return render_template('admin_dashboard.html', products=products, stats=stats)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def admin_add_product():
    if request.method == 'POST':
        new_product = {
            'id': max(p['id'] for p in products) + 1,
            'name': request.form.get('name'),
            'price': float(request.form.get('price', 0)),
            'category': request.form.get('category'),
            'stock': int(request.form.get('stock', 0)),
            'emoji': request.form.get('emoji', '🎁'),
            'img': request.form.get('img', ''),
            'desc': request.form.get('desc', ''),
        }
        products.append(new_product)
        flash(f'Product "{new_product["name"]}" added successfully! 🎉', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_add_product.html')

@app.route('/admin/products/delete/<int:product_id>')
@login_required
def admin_delete_product(product_id):
    global products
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        products = [p for p in products if p['id'] != product_id]
        flash(f'Product "{product["name"]}" deleted.', 'info')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
