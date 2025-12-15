from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
import re
from app.extensions import db
from app.blueprints.blog import bp
from app.blueprints.blog.forms import PostForm
from app.models.content import Post

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    next_url = url_for('blog.index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('blog.index', page=posts.prev_num) if posts.has_prev else None
    return render_template('blog/index.html', title='Blog', posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@bp.route('/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('blog/post.html', title=post.title, post=post)

from app.utils import save_picture

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        slug = slugify(form.title.data)
        if Post.query.filter_by(slug=slug).first():
            import time
            slug = f"{slug}-{int(time.time())}"
            
        cover_image_file = None
        if form.cover_image.data:
            cover_image_file = save_picture(form.cover_image.data)

        post = Post(title=form.title.data, 
                    content=form.content.data,
                    summary=form.summary.data,
                    cover_image=cover_image_file,
                    slug=slug, 
                    author=current_user,
                    status='published')
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('blog.index'))
    return render_template('blog/create_post.html', title='New Post', form=form)

@bp.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.role != 'admin':
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.summary = form.summary.data
        
        if form.cover_image.data:
            post.cover_image = save_picture(form.cover_image.data)
            
        # Optional: Update slug if title changes? better keep it stable for SEO or make it optional.
        # For now, let's keep slug stable.
        
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('blog.post', slug=post.slug))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.summary.data = post.summary
        
    return render_template('blog/edit_post.html', title='Update Post', form=form, legend='Update Post')
