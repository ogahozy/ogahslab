from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,\
    BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length,\
    Email, Regexp
from flask_pagedown.fields import PageDownField
from flask_babel import _, lazy_gettext as _l
from app.models import User, Role


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Usernames must have only letters, numbers, dots or '
               'underscores')])
    role = SelectField('Role', coerce=int)
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError(_l('Username already in use.'))


class PostForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired(_l("please enter title"))])
    post = PageDownField(_l('Write Your Post'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit Post'))


class SearchForm(FlaskForm):
    q = StringField(_l('Search'),validators=[DataRequired()])

    def __init__(self,*args,**kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm,self).__init__(*args,**kwargs)



class CommentForm(FlaskForm):
    body = StringField('Enter your Comment ', validators=[DataRequired()])
    submit = SubmitField('Submit')


#class MessageForm(FlaskForm):
 #   message = TextAreaField(_l('Message'), validators=[DataRequired(), Length(min=1, max=140)])
  #  submit = SubmitField(_l('Submit'))


