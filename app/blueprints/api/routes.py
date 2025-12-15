from flask import request, jsonify
from flask_login import login_required
from app.blueprints.api import bp
from app.services.ai_service import ai_service

@bp.route('/ai/format-post', methods=['POST'])
@login_required
def format_post():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400
    
    formatted_content = ai_service.format_post_content(content)
    return jsonify({'formatted_content': formatted_content})
