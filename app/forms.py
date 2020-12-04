from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, category


class RegistrationForm(FlaskForm):
    firstname = StringField('Ad*', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Soyad*', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    password = PasswordField('Şifrə*', validators=[DataRequired()])
    confirm_password = PasswordField('Təsdiq Şifrəsi*', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Qeydiyyatı Tamamla', render_kw={"style": "width:100%;"})

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Daxil etdiyiniz istifadəçi adı artıq istifadə olunub. Zəhmət olmasa, fərqli ad daxil edin. ')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Daxil etdiyiniz Email artıq istifadə olunub. Zəhmət olmasa, fərqli Email daxil edin.')


class LoginForm(FlaskForm):
    email = StringField('Email Ünvanı', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Ünvanı"})
    password = PasswordField('Şifrə', validators=[DataRequired()], render_kw={"placeholder": "Şifrə"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Hesabıma Daxil Ol', render_kw={"style": "width:100%;"})


class UpdateAccountForm(FlaskForm):
    username = StringField('İstifadəçi Adı', validators=[DataRequired(), Length(min=2, max=20)])
    firstname = StringField('Ad', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Soyad', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    # birthday = DateField('Doğum Tarixi', format='%Y-%m-%d', validators=[DataRequired()])
    # school = StringField('Təhsil Aldığınız Məktəb', validators=[Length(min=1, max=100)])
    # grade = SelectField(u'Təhsil pilləsi', choices  = [('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11')], coerce=int)
    # experience = TextAreaField('Riyaziyyat Olimpiadalarında Edindiyiniz Təcrübələr')
    picture = FileField('Profil şəklini yenilə', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Yenilə')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('Daxil etdiyiniz istifadəçi adı artıq istifadə olunub. Zəhmət olmasa, fərqli ad daxil edin.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('Daxil etdiyiniz Email artıq istifadə olunub. Zəhmət olmasa, fərqli Email daxil edin.')


class PostForm(FlaskForm):
    title = StringField('Başlıq', validators=[DataRequired()], render_kw={"placeholder": "Məqalənin Başlığı"})
    post_img = FileField('Məqaləni Təsvir edən Əsas Şəkili Əlavə Et', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Məqalənin Detalları', validators=[DataRequired()], render_kw={"placeholder": "Məqalənin Mətnini Bura Yazın...", "id": "textarea"})
    submit = SubmitField('Məqaləni Paylaş', render_kw={"style": "width:100%;"})

class BookForm(FlaskForm):
    name = StringField('Adı', validators=[DataRequired()])
    description = TextAreaField('Kitabın Təsviri', validators=[DataRequired()])
    url = TextAreaField('Kitabın Linki', validators=[DataRequired()])
    category = SelectField('Kitabın Kateqoriyası', choices = [(c.id, c.name) for c in category.query.all()])
    submit = SubmitField('Kitabı Əlavə Et')

class CatForm(FlaskForm):
    name = StringField('Adı', validators=[DataRequired()])
    submit = SubmitField('Kateqoriya Əlavə Et')