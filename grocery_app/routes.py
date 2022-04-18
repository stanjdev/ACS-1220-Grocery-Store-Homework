from unicodedata import name
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    # print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
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
            store_id = item_store
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

