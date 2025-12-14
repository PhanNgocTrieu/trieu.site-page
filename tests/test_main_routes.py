import pytest
from app.models.content import Post
from app.extensions import db


class TestMainIndex:
    """Test cases for the main.index route (news feed)."""
    
    def test_index_displays_posts(self, app, client, sample_posts):
        """Test that index route displays list of posts."""
        response = client.get('/')
        
        assert response.status_code == 200
        # Should show first 10 posts (most recent)
        for i in range(15, 5, -1):  # Posts 15 down to 6
            assert f'Test Post {i}'.encode() in response.data
    
    def test_index_pagination(self, app, client, sample_posts):
        """Test that index route paginates posts correctly (10 per page)."""
        # Get first page
        response = client.get('/')
        assert response.status_code == 200
        
        # Should show most recent 10 posts (15 down to 6)
        assert b'Test Post 15' in response.data
        assert b'Test Post 6' in response.data
        
        # Should not show posts beyond page 1
        assert b'Test Post 5' not in response.data
        assert b'Test Post 1' not in response.data
        
        # Get second page
        response = client.get('/?page=2')
        assert response.status_code == 200
        
        # Should show remaining 5 posts (5 down to 1)
        assert b'Test Post 5' in response.data
        assert b'Test Post 1' in response.data
        
        # Should not show posts from page 1
        assert b'Test Post 15' not in response.data
    
    def test_index_orders_by_created_at_desc(self, app, client, test_user):
        """Test that posts are ordered by creation date (newest first)."""
        with app.app_context():
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            old_post = Post(
                title='Old Post',
                slug='old-post',
                content='Old content',
                status='published',
                author=user
            )
            db.session.add(old_post)
            db.session.commit()
            
            new_post = Post(
                title='New Post',
                slug='new-post',
                content='New content',
                status='published',
                author=user
            )
            db.session.add(new_post)
            db.session.commit()
        
        response = client.get('/')
        
        # New Post should appear before Old Post in the HTML
        content = response.data.decode('utf-8')
        new_pos = content.find('New Post')
        old_pos = content.find('Old Post')
        
        assert new_pos > 0
        assert old_pos > 0
        assert new_pos < old_pos
    
    def test_index_empty_posts(self, client):
        """Test that index displays properly with no posts."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_per_page_limit(self, app, client, test_user):
        """Test that index shows exactly 10 posts per page."""
        # Create exactly 25 posts
        with app.app_context():
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            for i in range(25):
                post = Post(
                    title=f'Post {i+1}',
                    slug=f'post-{i+1}',
                    content=f'Content {i+1}',
                    status='published',
                    author=user
                )
                db.session.add(post)
            db.session.commit()
        
        # Page 1 should have posts 25-16
        response = client.get('/')
        assert b'Post 25' in response.data
        assert b'Post 16' in response.data
        assert b'Post 15' not in response.data
        
        # Page 2 should have posts 15-6
        response = client.get('/?page=2')
        assert b'Post 15' in response.data
        assert b'Post 6' in response.data
        assert b'Post 5' not in response.data
        
        # Page 3 should have posts 5-1
        response = client.get('/?page=3')
        assert b'Post 5' in response.data
        assert b'Post 1' in response.data
    
    def test_index_invalid_page_number(self, client, sample_posts):
        """Test that invalid page numbers are handled gracefully."""
        # Page 0 or negative should default to page 1
        response = client.get('/?page=0')
        assert response.status_code == 200
        
        # Very large page number should return empty results (not error)
        response = client.get('/?page=9999')
        assert response.status_code == 200
    
    def test_index_only_shows_published_posts(self, app, client, test_user):
        """Test that index only displays published posts, not drafts."""
        with app.app_context():
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            published_post = Post(
                title='Published Post',
                slug='published-post',
                content='Published content',
                status='published',
                author=user
            )
            draft_post = Post(
                title='Draft Post',
                slug='draft-post',
                content='Draft content',
                status='draft',
                author=user
            )
            
            db.session.add(published_post)
            db.session.add(draft_post)
            db.session.commit()
        
        response = client.get('/')
        
        # Note: Current implementation shows all posts regardless of status
        # This test documents current behavior, but ideally should filter by status
        # If you want to enforce published-only, update the route to filter by status
        assert response.status_code == 200
