from unicodedata import name
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_bcrypt import Bcrypt

from flask_login import login_required, login_user, logout_user, current_user
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.forms import GroceryStoreForm, GroceryItemForm, LoginForm, SignUpForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

bcrypt = Bcrypt(app)
main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(current_user)
    # print(all_stores)
    return render_template('home.html', all_stores=all_stores, current_user=current_user)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()
    # TODO: If form was submitted and was valid:
    if request.method == 'POST':
        store_title = request.form.get('title')
        store_address = request.form.get('address')

        # - create a new GroceryStore object and save it to the database,
        store = GroceryStore(
            title = store_title,
            address = store_address,
            created_by = current_user,
        )
        db.session.add(store)
        db.session.commit()
        # - flash a success message, and
        flash('Grocery store created!')
        # - redirect the user to the store detail page.
        return redirect(url_for('main.store_detail', store_id = store.id))
    else:
        # TODO: Send the form to the template and use it to render the form fields
        return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()
    # TODO: If form was submitted and was valid:
    if request.method == 'POST':
        item_name = request.form.get('name')
        item_price = request.form.get('price')
        item_category = request.form.get('category').upper()
        item_photo_url = request.form.get('photo_url')
        item_store = request.form.get('store')

    # - create a new GroceryItem object and save it to the database,
        item = GroceryItem(
            name = item_name,
            price = item_price,
            category = item_category,
            photo_url = item_photo_url,
            store_id = item_store,
            created_by = current_user,
        )
        db.session.add(item)
        db.session.commit()

        # - flash a success message, and
        flash('Item created.')
        # - redirect the user to the item detail page.
        return redirect(url_for('main.item_detail', item_id=item.id))
    else: 
        # TODO: Send the form to the template and use it to render the form fields
        return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    # TODO: If form was submitted and was valid:
    if request.method == 'POST':
    # - update the GroceryStore object and save it to the database,
        store.title = request.form.get('title')
        store.address = request.form.get('address')
        db.session.commit()
    # - flash a success message, and
        flash('Store was updated.')
        # - redirect the user to the store detail page.
        return redirect(url_for('main.store_detail', store_id = store.id))
    # TODO: Send the form to the template and use it to render the form fields
    else:
        # store = GroceryStore.query.get(store_id)
        return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    # TODO: If form was submitted and was valid:
    if request.method == 'POST':
    # - update the GroceryItem object and save it to the database,
        item.name = request.form.get('name')
        item.price = request.form.get('price')
        item.category = request.form.get('category').upper()
        item.photo_url = request.form.get('photo_url')
        item.store_id = request.form.get('store')
        db.session.commit()
    # - flash a success message, and
        flash('Item was updated successfully.')
    # - redirect the user to the item detail page.
        return redirect(url_for('main.item_detail', item_id = item.id))
    # TODO: Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', item=item, form=form)


@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
def add_to_shopping_list(item_id):
    # adds item to current_user's shopping list
    item = GroceryItem.query.filter_by(id=item_id).one()
    current_user.shopping_list_items.append(item)
    db.session.commit()
    return redirect(url_for('main.shopping_list'))

@main.route('/shopping_list')
@login_required
def shopping_list():
    items = current_user.shopping_list_items
    return render_template('shopping_list.html', items=items, current_user=current_user)


auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        found_user = User.query.filter_by(username=form.username.data).first()
        login_user(found_user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
