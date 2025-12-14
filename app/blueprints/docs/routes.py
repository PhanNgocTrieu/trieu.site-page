import os
from flask import render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.blueprints.docs import bp
from app.blueprints.docs.forms import UploadDocumentForm
from app.models.document import Document

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    documents = Document.query.order_by(Document.created_at.desc()).paginate(
        page=page, per_page=15, error_out=False)
    return render_template('docs/index.html', documents=documents.items, pagination=documents)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadDocumentForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        # Rename logic optional here, keeping original for docs usually preferred unless conflict
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'docs')
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
            
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        file_size = os.path.getsize(file_path)
        file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        doc = Document(title=form.title.data, filename=filename, 
                       file_type=file_type, file_size=file_size, uploader=current_user)
        db.session.add(doc)
        db.session.commit()
        
        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('docs.index'))
    return render_template('docs/upload.html', form=form)

@bp.route('/download/<int:doc_id>')
def download(doc_id):
    doc = Document.query.get_or_404(doc_id)
    directory = os.path.join(current_app.config['UPLOAD_FOLDER'], 'docs')
    return send_from_directory(directory, doc.filename, as_attachment=True)
