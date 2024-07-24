from flask import Flask
from flask_cors import CORS
from controllers.sentiment_controller import sentiment_blueprint
from controllers.document_controller import document_blueprint  

import torch
print(torch.__version__)

app = Flask(__name__)
CORS(app)  # Enable CORS to allow requests from other origins

# Register Blueprints
app.register_blueprint(sentiment_blueprint, url_prefix='/api')  
app.register_blueprint(document_blueprint, url_prefix='/api')  

if __name__ == '__main__':
    app.run(debug=True)
