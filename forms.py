from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import Length,DataRequired,Email

class Signupform(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=3)])
    password = PasswordField('password',validators=[DataRequired(),Length(min=3)])
    submit = SubmitField("Signup")

class Loginform(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=3)])
    password = PasswordField('password',validators=[DataRequired(),Length(min=3)])
    submit = SubmitField("Login")

class BlogForm(FlaskForm):
     filename = StringField('filename',validators=[DataRequired()])
     title = StringField('title',validators=[DataRequired()])
     blogText = TextAreaField('blogText',validators=[Length(min = 3)])
     create = SubmitField("create")

