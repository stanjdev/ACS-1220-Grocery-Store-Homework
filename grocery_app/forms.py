from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from .models import ItemCategory, GroceryStore

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField("Grocery Store Name:", validators=[DataRequired()])
    address = StringField("Address:", validators=[DataRequired()])
    submit = SubmitField("Submit")

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    CATEGORIES = ItemCategory
    # TODO: Add the following fields to the form class:
    name = StringField("Item Name:", validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired()])
    category = SelectField(u'Category', choices=CATEGORIES)
    photo_url = StringField("Photo URL:")
    store = SelectField(u'Store', choices = [(store.id, store.title) for store in GroceryStore.query.all()])
    # store = QuerySelectField('Store', 
    #     get_label='Grocery Store',
    #     allow_blank=False,
    #     blank_text='Select a store',
    #     render_kw={'size': 1},
    #     query_factory={}
    #     )
    submit = SubmitField("Submit")


