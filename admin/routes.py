from app import app, db
from app.models import User, Post, book, category
from flask import render_template, url_for, redirect, abort
from app.forms import BookForm, CatForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/admin')
@login_required
def admin_index():
    if User.query.get(1) == current_user:
        return render_template('/admin/starter.html')
    else:
        abort(403)

#Students

@app.route('/admin/tələbələr')
@login_required
def students():
    if User.query.get(1) == current_user:
        users = User.query.all()
        return render_template('/admin/students.html', users=users)
    else:
        abort(403)

@app.route('/admin/tələbələr/sil/<int:id>', methods = ['GET'])
@login_required
def delete_student(id):
    if User.query.get(1) == current_user:
        selectedPerson = User.query.get(id)
        db.session.delete(selectedPerson)
        db.session.commit()
        return redirect(url_for("students"))
    else:
        abort(403)

#Books

@app.route('/kitablar')
@login_required
def bookTable():
    if User.query.get(1) == current_user:
        books = book.query.all()
        categories = category.query.all()
        return render_template('/admin/bookTable.html', books=books, categories=categories)
    else:
        abort(403)

@app.route('/kitablar/əlavə-et', methods=['GET', 'POST'])
@login_required
def bookAddForm():
    if User.query.get(1) == current_user:
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
    else:
        abort(403)

@app.route('/admin/kitablar/kitab-sil/<int:id>', methods = ['GET'])
@login_required
def delete_book(id):
    if User.query.get(1) == current_user:
        selectedBook = book.query.get(id)
        db.session.delete(selectedBook)
        db.session.commit()
        return redirect(url_for("bookTable"))
    else:
        abort(403)
        
#Categories

@app.route('/kateqoriya-əlavə-et/yeni', methods=['GET', 'POST'])
@login_required
def addCategory():
    if User.query.get(1) == current_user:
        form = CatForm()
        if form.validate_on_submit():
            new_cat = category(name = form.name.data)
            db.session.add(new_cat)
            db.session.commit()
            return redirect(url_for('bookTable'))
        return render_template('/admin/addCategory.html', form=form)
    else:
        abort(403)

@app.route('/admin/kitablar/kateqoriya-sil/<int:id>', methods = ['GET'])
@login_required
def delete_cat(id):
    if User.query.get(1) == current_user:
        selectedCat = category.query.get(id)
        db.session.delete(selectedCat)
        db.session.commit()
        return redirect(url_for("bookTable"))
    else:
        abort(403)


@app.route('/advice-articles')
@login_required
def adviceForm():
    if User.query.get(1) == current_user:
        return render_template('/admin/adviceForm.html')
    else:
        abort(403)    