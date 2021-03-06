from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, SubmitField, BooleanField,TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Ingredient

#Formularz rejestracji
class RegistrationForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min = 2, max=20)]) #pierwszy argument to wyświetlana etykieta, drugi to ograniczenia nałożone na wprowadzoną wartosć
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up') #pole przesyłające dane z całego formularza

    #Funkcja służąca validowaniu rejestracji (czy nazwy i mail się nie powtarzają)
    def validate_username(self, username):

        user = User.query.filter_by(username = username.data).first() # sprawdzanie czy istnieje użytkownik o username wprowadzonym wlasnie do formularza rejestracji
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()  # sprawdzanie czy istnieje użytkownik o username wprowadzonym wlasnie do formularza rejestracji
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')

class ReceipeForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired(), Length(min = 2, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send receipe')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send comment')

class IngredientForm(FlaskForm):
    name = StringField('Nazwa składnika',
                         validators=[DataRequired(), Length(min = 2, max=100)])
    submit = SubmitField('Send Ingredient')

    #Funkcja służąca validowaniu dodawanego składnika
    def validate_name(self, name):

        ing = Ingredient.query.filter_by(name = name.data).first() # sprawdzanie czy istnieje użytkownik o username wprowadzonym wlasnie do formularza rejestracji
        if ing:
            raise ValidationError('This ingredient is already on the list')
