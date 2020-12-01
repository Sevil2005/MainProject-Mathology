from app import app, db
from app.models import User, Post, book, category
from flask import render_template, url_for, redirect
from app.forms import BookForm, CatForm


@app.route('/admin')
def admin_index():
    return render_template('/admin/starter.html')

@app.route('/admin/tələbələr')
def students():
    users = User.query.all()
    return render_template('/admin/students.html', users=users)

@app.route('/admin/tələbələr/sil/<int:id>/', methods = ['GET'])
def delete(id):
    selectedPerson = User.query.get(id)
    db.session.delete(selectedPerson)
    db.session.commit()
    return redirect(url_for("students"))


@app.route('/kitab-əlavə-et')
def bookTable():
    books = book.query.all()
    categories = category.query.all()
    return render_template('/admin/bookTable.html', books=books, categories=categories)

@app.route('/kitab-əlavə-et/yeni', methods=['GET', 'POST'])
def bookAddForm():
    categories = category.query.all()
    form = BookForm()
    if form.validate_on_submit():
        cat = form.category.data
        catObj = category.query.filter_by(id = cat).first()
        new_book = book(name = form.name.data, description = form.description.data, url = form.url.data, category = catObj)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('bookTable'))
    return render_template('/admin/bookAddForm.html', categories=categories, form=form)

@app.route('/kateqoriya-əlavə-et/yeni', methods=['GET', 'POST'])
def addCategory():
    form = CatForm()
    if form.validate_on_submit():
        new_cat = category(name = form.name.data)
        db.session.add(new_cat)
        db.session.commit()
        return redirect(url_for('bookTable'))
    return render_template('/admin/addCategory.html', form=form)


@app.route('/advice-articles')
def adviceForm():
    return render_template('/admin/adviceForm.html')