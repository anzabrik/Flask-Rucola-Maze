from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    DateTimeField,
    BooleanField,
    PasswordField,
)
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

from .models import *


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    remember = BooleanField("Remember me")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")


class IngredientForm(FlaskForm):
    name = StringField("Ingredient name", validators=[DataRequired()])
    quantity_available = StringField("Quantity available", validators=[DataRequired()])
    unit = StringField("Unit", validators=[DataRequired()], default="lb")
    unit_price_dollars = IntegerField(
        "Unit price: dollars", validators=[InputRequired()], default=0
    )
    unit_price_cents = StringField("cents", validators=[DataRequired()], default="00")
    submit = SubmitField("Save")


class MenuItemForm(FlaskForm):
    title = StringField("Menu item name", validators=[DataRequired()])
    price_dollars = IntegerField("Price, dollars", validators=[InputRequired()])
    price_cents = StringField("cents", validators=[DataRequired()], default="00")
    submit = SubmitField("Save")


class RecipeRequirementForm(FlaskForm):  # INCLUDE ONLY AVAILABLE ITEMS
    quantity_required = StringField("Quantity required", validators=[DataRequired()])
    all_ingredients_possible = QuerySelectField(label="Ingredient", allow_blank=False)
    all_menu_items_possible = QuerySelectField(label="Menu Item", allow_blank=False)

    submit = SubmitField("Save")


class PurchaseForm(FlaskForm):
    available_menu_items = QuerySelectField(label="Menu Item", allow_blank=False)
    submit = SubmitField("Save")
    pass
