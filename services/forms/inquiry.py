from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import Form
from wtforms import (
    IntegerField,
    StringField,
    validators,
    TextAreaField,
)


class InquiryForm(Form):
    name = StringField("Name", [validators.DataRequired()])
    email = StringField(
        "Email Address", [validators.Length(min=6, max=35), validators.Email()]
    )
    subject = StringField("Subject", [validators.DataRequired()])
    msg = TextAreaField("Description", [validators.DataRequired()])
