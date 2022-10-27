from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length
)


class RegistrationForm(FlaskForm):
    """Register form"""
    email = EmailField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match'),
        Length(8, 20)
    ], render_kw={"placeholder": "Password"})
    confirm = PasswordField('Repeat Password', validators=[
        DataRequired(),
        Length(8, 20)
    ], render_kw={"placeholder": "Re-type Password"})
