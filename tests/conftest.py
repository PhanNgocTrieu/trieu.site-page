import os
import pytest
import tempfile
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.document import Document
from app.models.content import Post


@pytest.fixture(scope='function')
def app():
    """Create and configure a test application instance."""
    # Create a temporary file for the test database
    db_fd, db_path = tempfile.mkstemp()
    
    # Create a temporary upload folder
    upload_folder = tempfile.mkdtemp()
    
    app = create_app('default')
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,  # Disable CSRF for testing
        'UPLOAD_FOLDER': upload_folder,
        'SECRET_KEY': 'test-secret-key'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def test_user(app):
    """Create a test user."""
    with app.app_context():
        user = User(username='testuser', email='test@example.com', role='user')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
        
        # Refresh to get the ID
        db.session.refresh(user)
        user_id = user.id
        
    return {'id': user_id, 'username': 'testuser', 'password': 'testpassword'}


@pytest.fixture(scope='function')
def authenticated_client(client, test_user):
    """Create a client authenticated with test_user."""
    client.post('/auth/login', data={
        'username': test_user['username'],
        'password': test_user['password']
    }, follow_redirects=True)
    return client


@pytest.fixture(scope='function')
def sample_posts(app, test_user):
    """Create sample posts for testing."""
    with app.app_context():
        user = User.query.get(test_user['id'])
        posts = []
        for i in range(15):
            post = Post(
                title=f'Test Post {i+1}',
                slug=f'test-post-{i+1}',
                content=f'Content for post {i+1}',
                summary=f'Summary {i+1}',
                status='published',
                author=user
            )
            posts.append(post)
            db.session.add(post)
        db.session.commit()
        
    return posts
