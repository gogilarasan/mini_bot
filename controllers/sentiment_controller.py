from flask import Blueprint, request, jsonify
from models.sentiment_model import analyze_text, analyze_emoji

sentiment_blueprint = Blueprint('sentiment', __name__)

@sentiment_blueprint.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()  # Get data from POST request
    text = data.get('text', '')

    sentiment = analyze_text(text)  # Analyze text sentiment
    emoji_score = analyze_emoji(text)  # Analyze emoji sentiment

    # Combine results
    sentiment['emoji_pos'] = emoji_score['pos']
    sentiment['emoji_neg'] = emoji_score['neg']
    sentiment['emoji_neutral'] = emoji_score['neutral']

    return jsonify(sentiment)  # Return results as JSON
