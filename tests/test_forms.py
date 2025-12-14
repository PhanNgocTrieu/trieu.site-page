import io
import pytest
from werkzeug.datastructures import FileStorage
from app.blueprints.docs.forms import UploadDocumentForm


class TestUploadDocumentForm:
    """Test cases for UploadDocumentForm validation."""
    
    def test_form_valid_with_all_fields(self, app):
        """Test that form is valid with all required fields."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='test.pdf',
                    content_type='application/pdf'
                )
            )
            
            assert form.validate() is True
    
    def test_form_invalid_without_title(self, app):
        """Test that form is invalid when title is missing."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='test.pdf',
                    content_type='application/pdf'
                )
            )
            
            assert form.validate() is False
            assert 'title' in form.errors
    
    def test_form_invalid_without_file(self, app):
        """Test that form is invalid when file is missing."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=None
            )
            
            assert form.validate() is False
            assert 'file' in form.errors
    
    def test_form_accepts_pdf_files(self, app):
        """Test that form accepts PDF files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='document.pdf',
                    content_type='application/pdf'
                )
            )
            
            assert form.validate() is True
    
    def test_form_accepts_doc_files(self, app):
        """Test that form accepts DOC files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='document.doc',
                    content_type='application/msword'
                )
            )
            
            assert form.validate() is True
    
    def test_form_accepts_docx_files(self, app):
        """Test that form accepts DOCX files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='document.docx',
                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                )
            )
            
            assert form.validate() is True
    
    def test_form_accepts_ppt_files(self, app):
        """Test that form accepts PPT files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='presentation.ppt',
                    content_type='application/vnd.ms-powerpoint'
                )
            )
            
            assert form.validate() is True
    
    def test_form_accepts_pptx_files(self, app):
        """Test that form accepts PPTX files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='presentation.pptx',
                    content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
                )
            )
            
            assert form.validate() is True
    
    def test_form_accepts_xls_files(self, app):
        """Test that form accepts XLS files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='spreadsheet.xls',
                    content_type='application/vnd.ms-excel'
                )
            )
            
            assert form.validate() is True
    
    def test_form_accepts_xlsx_files(self, app):
        """Test that form accepts XLSX files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='spreadsheet.xlsx',
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            )
            
            assert form.validate() is True
    
    def test_form_accepts_txt_files(self, app):
        """Test that form accepts TXT files."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='document.txt',
                    content_type='text/plain'
                )
            )
            
            assert form.validate() is True
    
    def test_form_rejects_disallowed_file_types(self, app):
        """Test that form rejects non-document file types."""
        disallowed_files = [
            ('image.jpg', 'image/jpeg'),
            ('script.py', 'text/x-python'),
            ('video.mp4', 'video/mp4'),
            ('audio.mp3', 'audio/mpeg'),
            ('archive.zip', 'application/zip'),
            ('executable.exe', 'application/x-msdownload')
        ]
        
        for filename, content_type in disallowed_files:
            with app.test_request_context():
                form = UploadDocumentForm(
                    title='Test Document',
                    file=FileStorage(
                        stream=io.BytesIO(b'test content'),
                        filename=filename,
                        content_type=content_type
                    )
                )
                
                assert form.validate() is False, f'{filename} should be rejected'
                assert 'file' in form.errors
    
    def test_form_file_extension_validation_case_insensitive(self, app):
        """Test that file extension validation is case-insensitive."""
        extensions = ['PDF', 'Pdf', 'pDf', 'DOCX', 'TXT']
        
        for ext in extensions:
            with app.test_request_context():
                form = UploadDocumentForm(
                    title='Test Document',
                    file=FileStorage(
                        stream=io.BytesIO(b'test content'),
                        filename=f'document.{ext}',
                        content_type='application/octet-stream'
                    )
                )
                
                assert form.validate() is True, f'.{ext} extension should be accepted'
    
    def test_form_rejects_file_without_extension(self, app):
        """Test that form rejects files without extensions."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='Test Document',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='document_no_extension',
                    content_type='application/octet-stream'
                )
            )
            
            assert form.validate() is False
            assert 'file' in form.errors
    
    def test_form_title_field_required(self, app):
        """Test that title field has DataRequired validator."""
        with app.test_request_context():
            form = UploadDocumentForm()
            
            # Check that title field has validators
            title_validators = [v.__class__.__name__ for v in form.title.validators]
            assert 'DataRequired' in title_validators
    
    def test_form_file_field_required(self, app):
        """Test that file field has FileRequired validator."""
        with app.test_request_context():
            form = UploadDocumentForm()
            
            # Check that file field has validators
            file_validators = [v.__class__.__name__ for v in form.file.validators]
            assert 'FileRequired' in file_validators
            assert 'FileAllowed' in file_validators
    
    def test_form_multiple_validation_errors(self, app):
        """Test that form can have multiple validation errors at once."""
        with app.test_request_context():
            form = UploadDocumentForm(
                title='',
                file=FileStorage(
                    stream=io.BytesIO(b'test content'),
                    filename='malicious.exe',
                    content_type='application/x-msdownload'
                )
            )
            
            assert form.validate() is False
            assert 'title' in form.errors
            assert 'file' in form.errors
            assert len(form.errors) == 2
