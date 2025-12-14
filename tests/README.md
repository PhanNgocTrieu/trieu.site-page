# Tests

This directory contains unit tests for the application.

## Setup

Install test dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run a specific test file:

```bash
pytest tests/test_docs_routes.py
```

Run a specific test class:

```bash
pytest tests/test_docs_routes.py::TestDocsUpload
```

Run a specific test:

```bash
pytest tests/test_docs_routes.py::TestDocsUpload::test_upload_document_success
```

## Test Coverage

Run tests with coverage report:

```bash
pytest --cov=app --cov-report=html
```

## Test Structure

- `conftest.py` - Pytest fixtures and test configuration
- `test_docs_routes.py` - Tests for document routes (upload, download, index)
- `test_main_routes.py` - Tests for main routes (news feed)
- `test_forms.py` - Tests for form validation

## Test Cases

### Document Upload (`test_docs_routes.py::TestDocsUpload`)
- Upload requires authentication
- Upload form displays correctly
- Document upload saves file and creates database record
- Upload creates directory if needed
- Filename sanitization

### Document Download (`test_docs_routes.py::TestDocsDownload`)
- Download existing document
- Download non-existent document returns 404
- Correct file is served

### Document Index (`test_docs_routes.py::TestDocsIndex`)
- Displays document list
- Pagination (15 per page)
- Ordered by creation date (newest first)
- Empty list handling

### Main Index (`test_main_routes.py::TestMainIndex`)
- Displays post list
- Pagination (10 per page)
- Ordered by creation date (newest first)
- Invalid page number handling
- Empty posts handling

### Form Validation (`test_forms.py::TestUploadDocumentForm`)
- Required fields validation
- Allowed file types (pdf, doc, docx, ppt, pptx, xls, xlsx, txt)
- Rejected file types (images, scripts, executables, etc.)
- Case-insensitive extension validation
- Multiple validation errors
