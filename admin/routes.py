from app import app, db
from app.models import User, Post
from flask import render_template, url_for, redirect


@app.route('/admin')
def admin_index():
    return render_template('/admin/starter.html')

@app.route('/admin/students')
def students():
    users = User.query.all()
    return render_template('/admin/students.html', users=users)

@app.route('/admin/students/delete/<int:id>/', methods = ['GET'])
def delete(id):
    selectedPerson = User.query.get(id)
    db.session.delete(selectedPerson)
    db.session.commit()
    return redirect(url_for("students"))