from flask import Blueprint, request, jsonify
from models.document_model import extract_text_from_pdf, extract_text_from_docx, summarize_text, answer_question
import logging

document_blueprint = Blueprint('document', __name__)

@document_blueprint.route('/upload', methods=['POST'])
def upload_document():
    try:
        file = request.files['file']
        detail_level = request.form.get('detail_level', 'brief')  # Default to brief if not provided
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(file)
        else:
            response = jsonify({'error': 'Unsupported file type'})
            logging.info(f'Response: {response.get_json()}')
            return response, 400

        summary = summarize_text(text, detail_level)
        response = jsonify({'summary': summary, 'text': text})
        logging.info(f'Response: {response.get_json()}')
        return response
    except Exception as e:
        logging.error(f"Error in upload_document: {e}")
        response = jsonify({'error': 'An error occurred during document upload.'})
        logging.info(f'Response: {response.get_json()}')
        return response, 500

@document_blueprint.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        context = data['context']
        question = data['question']
        if not context or not question:
            response = jsonify({'error': 'Context and question are required'})
            logging.info(f'Response: {response.get_json()}')
            return response, 400
        answer = answer_question(context, question)
        response = jsonify({'answer': answer})
        logging.info(f'Response: {response.get_json()}')
        return response
    except Exception as e:
        logging.error(f"Error in ask_question: {e}")
        response = jsonify({'error': 'An error occurred during question answering.'})
        logging.info(f'Response: {response.get_json()}')
        return response, 500
