from flask_wtf.file import FileAllowed, FileField
from flask_wtf import Form
from wtforms import validators


class UpdateCarousel(Form):
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
    image_3 = FileField(
        "Image 4",
        validators=[
            validators.Optional(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )
    image_4 = FileField(
        "Image 5",
        validators=[
            validators.Optional(),
            FileAllowed(["jpg", "png", "gif", "jpeg"], "Images only please"),
        ],
    )


class UpdatePromoProducts(Form):
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