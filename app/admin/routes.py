from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
import os
from app import db 
from werkzeug.utils import secure_filename
from  app.models import Post, Users

admin_bp = Blueprint('admin', __name__)

"""PÁGINAS"""

@admin_bp.route('/')
def dashboard():
    total_posts = Post.query.count()
    total_users = Users.query.count()
    return render_template('admin/dashboard.html', total_posts=total_posts, total_users=total_users)

@admin_bp.route('/posts')
def posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@admin_bp.route("/users")
def users():
    users = Users.query.order_by(Users.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

"""GESTÃO DE USUSARIOS"""

@admin_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        flash('Usuario atualizado!')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/users.html', user=user)

@admin_bp.route('delete-user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario excluído com sucesso!')
    return redirect(url_for('admin.users'))

"""GESTÃO DE POSTS"""

# NOVO POST
@admin_bp.route('/new-post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        flash('Post criado com sucesso!')
        return redirect(url_for('main.index'))
    return render_template('admin/new_post.html')

# EDITAR POST
@admin_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        flash('Post atualizado!')
        return redirect(url_for('admin.posts'))
    return render_template('admin/edit_post.html', post=post)

# DELETAR POST
@admin_bp.route('/delete-post/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post excluído com sucesso!')
    return redirect(url_for('admin.posts'))
