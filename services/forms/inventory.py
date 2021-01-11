from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import Form
from wtforms import (
    IntegerField,
    StringField,
    validators,
    TextAreaField,
)


class AddProduct(Form):
    name = StringField("Name", [validators.DataRequired()])
    centprice = IntegerField(
        "Price",
        [
            validators.InputRequired(message="Please enter a valid integer value."),
            validators.NumberRange(min=0, max=999999999),
        ],
    )
    discount = IntegerField(
        "Discount",
        validators=[
            validators.InputRequired(message="Please enter a valid integer value."),
            validators.NumberRange(min=0, max=100),
        ],
    )
    stock = IntegerField(
        "Stock",
        [
            validators.InputRequired(message="Please enter a valid integer value."),
            validators.NumberRange(min=0, max=999999999),
        ],
    )
    desc = TextAreaField("Description", [validators.DataRequired()])

    image_0 = FileField(
        "Image 1",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )
    image_1 = FileField(
        "Image 2",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )
    image_2 = FileField(
        "Image 3",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )


class UpdateProduct(Form):
    name = StringField("Name", [validators.Optional()])
    centprice = IntegerField(
        "Price",
        [
            validators.Optional(),
            validators.NumberRange(min=0, max=999999999),
        ],
    )
    discount = IntegerField(
        "Discount",
        validators=[
            validators.Optional(),
            validators.NumberRange(min=0, max=100),
        ],
    )
    stock = IntegerField(
        "Stock",
        [
            validators.Optional(),
            validators.NumberRange(min=0, max=999999999),
        ],
    )
    desc = TextAreaField("Description", [validators.Optional()])

    image_0 = FileField(
        "Image 1",
        validators=[
            validators.Optional(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )
    image_1 = FileField(
        "Image 2",
        validators=[
            validators.Optional(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )
    image_2 = FileField(
        "Image 3",
        validators=[
            validators.Optional(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )


class AddBrand(Form):
    name = StringField("Name", [validators.DataRequired()])
    desc = TextAreaField("Description", [validators.DataRequired()])


class AddCategory(Form):
    name = StringField("Name", [validators.DataRequired()])
    desc = TextAreaField("Description", [validators.DataRequired()])