import os
import smtplib
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from app.models import User, Post, book, category
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


@app.route('/')
@app.route('/ana-səhifə')
def home():
    return render_template('app/home.html')

@app.route('/haqqımızda')
def about():
    return render_template('app/about.html', title='Haqqımızda')

# Login-Register

@app.route("/qeydiyyat", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=hashed_password)
        user.username = f"{user.firstname} {user.lastname}"
        db.session.add(user)
        db.session.commit()
        flash('Hesabınız uğurla yaradıldı! İndi Daxil Ola bilərsiz.', 'success')

        return redirect(url_for('login'))
    return render_template('app/register.html', title='Qeydiyyat', form=form)


@app.route("/daxil-ol", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Daxil Olma sorğunuz uğursuz oldu. Zəhmət olmasa email və şifrəni bir daha yoxlayın.', 'danger')
    return render_template('app/login.html', title='Daxil Ol', form=form)


@app.route("/çıxış")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture_user(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    path = os.path.dirname(app.instance_path)
    picture_path = os.path.join(path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/hesabım", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_user(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Hesab Məlumatlarınız Yeniləndi!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('app/user/account.html', title='Hesabım', image_file=image_file, form=form)


# Blog

@app.route('/məsləhət-bloqu')
def blog():
    posts = Post.query.order_by(Post.date_posted.desc())
    return render_template('app/adviceBlog/blog.html', title="Məsləhət Bloqu", posts=posts)


@app.route("/məsləhət-bloqu/yeni-məqalə-yaz", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Yeni məqalə haqqında sorğu sistemə uğurla göndərildi!', 'success')
        return redirect(url_for('blog'))
    return render_template('app/adviceBlog/create_post.html', title="Yeni Məqalə", form=form)


@app.route("/məsləhət-bloqu/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('app/adviceBlog/post_details.html', title=post.title, post=post)


@app.route("/məsləhət-bloqu/<int:post_id>/redaktə-et", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Məqaləniz uğurla redaktə olundu!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method =='GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('app/adviceBlog/create_post.html', title="Məqaləni Redaktə Et", form=form, legend='Məqaləni Redaktə Et')

@app.route("/məsləhət-bloqu/<int:post_id>/sil", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Məqaləniz silindi!', 'success')
    return redirect(url_for('blog'))


@app.route("/istifadəçi/<string:username>")
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc())
    return render_template('app/adviceBlog/user_posts.html', posts=posts, user=user)

# Books

@app.route('/olimpiadalar/<int:id>')
def olympiads(id):
    books = book.query.filter_by(category_id=id)
    cat = category.query.filter_by(id=id).first()
    return render_template('app/books/book.html', title=cat.name, books=books)