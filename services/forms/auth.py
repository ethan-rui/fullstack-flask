from wtforms import StringField, Form, PasswordField, validators


class RegistrationForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField(
        "Email Address", [validators.Length(min=6, max=35), validators.Email()]
    )
    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
            validators.length(
                min=8, max=32, message="Password must be at least 8 characters"
            ),
        ],
    )
    confirm = PasswordField("Repeat Password")


class LoginForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.DataRequired()])


class ProfileForm(Form):
    street = StringField(
        "Street", [validators.DataRequired(), validators.Length(min=4, max=25)]
    )
    unit_no = StringField(
        "Unit No.", [validators.DataRequired(), validators.Length(min=3, max=25)]
    )
    pcode = StringField(
        "Postal code", [validators.DataRequired(), validators.Length(min=4, max=25)]
    )


class PswUpdateForm(Form):
    oldpassword = PasswordField("Old Password", [validators.DataRequired()])

    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password")