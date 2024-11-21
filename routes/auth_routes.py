import os
from flask import Blueprint, request, jsonify, redirect, make_response
from services.auth_service import exchange_code_for_token, fetch_user_profile
import jwt

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/amazon', methods=['GET'])
def amazon_login():
    """Redirects user to Amazon login page."""
    amazon_auth_url = (
        f"https://www.amazon.com/ap/oa?"
        f"client_id={os.getenv('LWA_CLIENT_ID')}&"
        f"scope=profile&"
        f"response_type=code&"
        f"redirect_uri={os.getenv('LWA_REDIRECT_URI')}"
    )
    return redirect(amazon_auth_url)


@auth_blueprint.route('/amazon/callback', methods=['GET'])
def amazon_login_callback():
    """Handles Amazon callback and exchanges code for access token."""
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'Authorization code is missing'}), 400

    try:
        access_token = exchange_code_for_token(code)
        user_profile = fetch_user_profile(access_token)
        jwt_token = jwt.encode(user_profile, os.getenv('JWT_SECRET'), algorithm='HS256')

        frontend_url = os.getenv('FRONTEND_REDIRECT_URL', 'http://localhost:3000/login/callback')
        response = make_response(redirect(frontend_url))
        response.set_cookie('access_token', jwt_token, httponly=True, secure=True, samesite='Lax')

        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@auth_blueprint.route('/profile', methods=['GET'])
def decode_token():
    try:
        token = request.cookies.get('access_token')
        print(type(token))
        if not token:
            return jsonify({"error": "No access token found in cookies"}), 401
        decoded_token = jwt.decode(token,os.getenv('JWT_SECRET'), algorithms=["HS256"])  # Use your signing algorithm
        return jsonify({"profile": decoded_token}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
