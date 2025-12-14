import os
import io
import pytest
from app.models.document import Document
from app.extensions import db


class TestDocsUpload:
    """Test cases for the docs.upload route."""
    
    def test_upload_requires_authentication(self, client):
        """Test that upload route requires authentication."""
        response = client.get('/docs/upload')
        # Should redirect to login
        assert response.status_code == 302
        assert '/auth/login' in response.location
    
    def test_upload_get_displays_form(self, authenticated_client):
        """Test that GET request displays upload form."""
        response = authenticated_client.get('/docs/upload')
        assert response.status_code == 200
        assert b'Upload' in response.data
    
    def test_upload_document_success(self, app, authenticated_client, test_user):
        """Test successful document upload saves file and creates database record."""
        # Create a fake PDF file
        data = {
            'title': 'Test Document',
            'file': (io.BytesIO(b'PDF content here'), 'test_doc.pdf')
        }
        
        response = authenticated_client.post(
            '/docs/upload',
            data=data,
            content_type='multipart/form-data',
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert b'Document uploaded successfully!' in response.data
        
        # Verify file was saved to filesystem
        with app.app_context():
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'docs', 'test_doc.pdf')
            assert os.path.exists(upload_path)
            
            # Verify database record was created
            doc = Document.query.filter_by(title='Test Document').first()
            assert doc is not None
            assert doc.filename == 'test_doc.pdf'
            assert doc.file_type == 'pdf'
            assert doc.file_size > 0
            assert doc.user_id == test_user['id']
    
    def test_upload_creates_directory_if_not_exists(self, app, authenticated_client):
        """Test that upload creates the docs directory if it doesn't exist."""
        # Remove the docs directory if it exists
        docs_path = os.path.join(app.config['UPLOAD_FOLDER'], 'docs')
        if os.path.exists(docs_path):
            os.rmdir(docs_path)
        
        data = {
            'title': 'Test Document',
            'file': (io.BytesIO(b'File content'), 'test.pdf')
        }
        
        response = authenticated_client.post(
            '/docs/upload',
            data=data,
            content_type='multipart/form-data',
            follow_redirects=True
        )
        
        assert response.status_code == 200
        assert os.path.exists(docs_path)
    
    def test_upload_sanitizes_filename(self, app, authenticated_client):
        """Test that upload sanitizes potentially dangerous filenames."""
        data = {
            'title': 'Test Document',
            'file': (io.BytesIO(b'Content'), '../../../etc/passwd.pdf')
        }
        
        response = authenticated_client.post(
            '/docs/upload',
            data=data,
            content_type='multipart/form-data',
            follow_redirects=True
        )
        
        with app.app_context():
            # Should be sanitized to just 'passwd.pdf' or 'etc_passwd.pdf'
            doc = Document.query.filter_by(title='Test Document').first()
            assert doc is not None
            assert '..' not in doc.filename
            assert '/' not in doc.filename


class TestDocsDownload:
    """Test cases for the docs.download route."""
    
    def test_download_existing_document(self, app, client, test_user):
        """Test downloading an existing document returns the file."""
        # Create a document record and file
        with app.app_context():
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'docs')
            os.makedirs(upload_path, exist_ok=True)
            
            file_path = os.path.join(upload_path, 'test_download.pdf')
            with open(file_path, 'wb') as f:
                f.write(b'Test PDF content')
            
            user = db.session.get(db.select(type('User', (), {'id': test_user['id']})).columns(type('User', (), {'id': test_user['id']}).__dict__.get('id')))
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            doc = Document(
                title='Test Download',
                filename='test_download.pdf',
                file_type='pdf',
                file_size=16,
                uploader=user
            )
            db.session.add(doc)
            db.session.commit()
            doc_id = doc.id
        
        # Download the document
        response = client.get(f'/docs/download/{doc_id}')
        
        assert response.status_code == 200
        assert response.data == b'Test PDF content'
        assert 'attachment' in response.headers.get('Content-Disposition', '')
    
    def test_download_nonexistent_document(self, client):
        """Test downloading a non-existent document returns 404."""
        response = client.get('/docs/download/99999')
        assert response.status_code == 404
    
    def test_download_serves_correct_file(self, app, client, test_user):
        """Test that download serves the correct file for the requested document."""
        with app.app_context():
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'docs')
            os.makedirs(upload_path, exist_ok=True)
            
            # Create two different files
            file1_path = os.path.join(upload_path, 'doc1.txt')
            with open(file1_path, 'wb') as f:
                f.write(b'Document 1 content')
            
            file2_path = os.path.join(upload_path, 'doc2.txt')
            with open(file2_path, 'wb') as f:
                f.write(b'Document 2 content')
            
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            doc1 = Document(title='Doc 1', filename='doc1.txt', file_type='txt', 
                          file_size=18, uploader=user)
            doc2 = Document(title='Doc 2', filename='doc2.txt', file_type='txt',
                          file_size=18, uploader=user)
            
            db.session.add(doc1)
            db.session.add(doc2)
            db.session.commit()
            
            doc1_id = doc1.id
            doc2_id = doc2.id
        
        # Download doc1
        response1 = client.get(f'/docs/download/{doc1_id}')
        assert response1.data == b'Document 1 content'
        
        # Download doc2
        response2 = client.get(f'/docs/download/{doc2_id}')
        assert response2.data == b'Document 2 content'


class TestDocsIndex:
    """Test cases for the docs.index route."""
    
    def test_index_displays_document_list(self, app, client, test_user):
        """Test that index route displays list of documents."""
        # Create some test documents
        with app.app_context():
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            for i in range(5):
                doc = Document(
                    title=f'Document {i+1}',
                    filename=f'doc{i+1}.pdf',
                    file_type='pdf',
                    file_size=1000,
                    uploader=user
                )
                db.session.add(doc)
            db.session.commit()
        
        response = client.get('/docs/')
        
        assert response.status_code == 200
        for i in range(5):
            assert f'Document {i+1}'.encode() in response.data
    
    def test_index_pagination(self, app, client, test_user):
        """Test that index route paginates documents correctly."""
        # Create more documents than per_page (15)
        with app.app_context():
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            for i in range(20):
                doc = Document(
                    title=f'Document {i+1}',
                    filename=f'doc{i+1}.pdf',
                    file_type='pdf',
                    file_size=1000,
                    uploader=user
                )
                db.session.add(doc)
            db.session.commit()
        
        # Get first page
        response = client.get('/docs/')
        assert response.status_code == 200
        
        # Should show most recent 15 documents (20 down to 6)
        assert b'Document 20' in response.data
        assert b'Document 6' in response.data
        
        # Get second page
        response = client.get('/docs/?page=2')
        assert response.status_code == 200
        
        # Should show remaining 5 documents (5 down to 1)
        assert b'Document 5' in response.data
        assert b'Document 1' in response.data
    
    def test_index_orders_by_created_at_desc(self, app, client, test_user):
        """Test that documents are ordered by creation date (newest first)."""
        with app.app_context():
            from app.models.user import User
            user = User.query.get(test_user['id'])
            
            doc1 = Document(title='Old Document', filename='old.pdf', 
                          file_type='pdf', file_size=1000, uploader=user)
            db.session.add(doc1)
            db.session.commit()
            
            doc2 = Document(title='New Document', filename='new.pdf',
                          file_type='pdf', file_size=1000, uploader=user)
            db.session.add(doc2)
            db.session.commit()
        
        response = client.get('/docs/')
        
        # New Document should appear before Old Document in the HTML
        content = response.data.decode('utf-8')
        new_pos = content.find('New Document')
        old_pos = content.find('Old Document')
        
        assert new_pos > 0
        assert old_pos > 0
        assert new_pos < old_pos
    
    def test_index_empty_list(self, client):
        """Test that index displays properly with no documents."""
        response = client.get('/docs/')
        assert response.status_code == 200
