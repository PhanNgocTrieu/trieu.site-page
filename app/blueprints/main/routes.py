from flask import render_template, request
from app.models.content import Post
from app.blueprints.main import bp

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # Get latest posts, paginated
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('index.html', posts=posts.items, pagination=posts)
