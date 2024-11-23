from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routes.auth_routes import auth_blueprint

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Flask app
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_COOKIE_SECURE'] = True
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Register Blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
