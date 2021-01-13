from wtforms import StringField, validators, TextAreaField, Form


class InquiryForm(Form):
    sender_name = StringField("Name", [validators.DataRequired()])
    sender_email = StringField(
        "Email Address",
        [
            validators.Length(min=6, max=35),
            validators.Email(),
            validators.DataRequired(),
        ],
    )
    subject = StringField("Subject", [validators.DataRequired()])
    content = TextAreaField("Description", [validators.DataRequired()])
