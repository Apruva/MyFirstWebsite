from wtforms import StringField, PasswordField, SubmitField, validators, TextAreaField, TextField, DateField, \
    IntegerField, SelectMultipleField
from wtforms.fields.html5 import DateTimeField
from wtforms.widgets import TextArea
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from web_app.models import Subscribers, Users
from web_app.routes import flash


class SubForm(FlaskForm):
    email = StringField('Email Address',
                        validators=[DataRequired(), validators.Length(min=5, max=25),
                                    EqualTo("confirm_email", message="Email must match!")])

    confirm_email = StringField('Confirm Email',
                                validators=[DataRequired(), validators.Length(min=5, max=25),
                                            EqualTo("email", message="Email must match!")])

    submit = SubmitField("Subscribe")

    def validate_email(self, email):
        user = Subscribers.query.filter_by(email=email.data).first()
        if user:
            flash("Email already in use!", "danger")
            raise ValidationError()


class RegForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       EqualTo("confirm_username", message="Username must match!"),
                                       validators.Length(min=8, max=25),
                                       validators.Regexp('^[a-zA-Z0-9]+$',
                                                         message="Special characters not allowed!")])
    confirm_username = StringField("Confirm username",
                                   validators=[DataRequired(),
                                               EqualTo("username", message="Username must match!"),
                                               validators.Length(min=8, max=25),
                                               validators.Regexp('^[a-zA-Z0-9]+$',
                                                                 message="Special characters not allowed!")])

    password = PasswordField("Password",
                             validators=[DataRequired(), EqualTo("confirm_password", message="Password must match!"),
                                         validators.Length(min=8, max=25)])

    confirm_password = PasswordField("Confirm password",
                                     validators=[DataRequired(), EqualTo("password", message="Password must match!"),
                                                 validators.Length(min=8, max=25)])

    mail = StringField('Email Address',
                       validators=[DataRequired(), validators.Length(min=6, max=25),
                                   EqualTo("confirm_mail", message="Email must match!")])

    confirm_mail = StringField('Confirm Email',
                               validators=[DataRequired(), validators.Length(min=6, max=25),
                                           EqualTo("mail", message="Email must match!")])

    submit = SubmitField("Register")

    def validate_username(self, username):
        username = Users.query.filter_by(username=username.data).first()
        if username:
            flash("Username exists!", "danger")
            raise ValidationError()

    def validate_mail(self, mail):
        mail = Users.query.filter_by(mail=mail.data).first()
        if mail:
            flash("Email already in use!", "danger")
            raise ValidationError()


class LogForm(FlaskForm):
    mail = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UpdateForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       validators.Length(min=8, max=25),
                                       validators.Regexp('^[a-zA-Z0-9]+$',
                                                         message="Special characters not allowed!")])
    mail = StringField('Email',
                       validators=[DataRequired(), validators.Length(min=6, max=25)])

    picture = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken!")

    def validate_mail(self, mail):
        if mail.data != current_user.mail:
            user = Users.query.filter_by(mail=mail.data).first()
            if user:
                raise ValidationError("Email is already taken!")


class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), validators.Length(min=10)])
    content = TextAreaField('Post Content', validators=[DataRequired(), validators.length(min=10)])
    submit = SubmitField('Submit Post')


class TodoForm(FlaskForm):
    comment = TextAreaField('Comment',
                            validators=[DataRequired(), validators.length(min=5)], default="To-do message",
                            widget=TextArea())
    priority = StringField('Priority (low-high)',
                           validators=[DataRequired()], default="None")
    submit = SubmitField('Add to-do')


class RatesForm(FlaskForm):
    rate = StringField('Currency',
                       validators=[DataRequired(),
                                   validators.length(min=3, max=3, message='Must be three characters!')], default='NOK')
    base = StringField('Base Currency',
                       validators=[DataRequired(),
                                   validators.length(min=3, max=3, message='Must be three characters!')],
                       default='EUR')
    submit = SubmitField('Get Rate')
