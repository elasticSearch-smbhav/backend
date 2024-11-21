import requests
import os

def exchange_code_for_token(code):
    """Exchanges authorization code for access token."""
    url = 'https://api.amazon.com/auth/o2/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': os.getenv('LWA_CLIENT_ID'),
        'client_secret': os.getenv('LWA_CLIENT_SECRET'),
        'redirect_uri': os.getenv('LWA_REDIRECT_URI'),
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json().get('access_token')


def fetch_user_profile(access_token):
    """Fetches the user profile using the access token."""
    url = 'https://api.amazon.com/user/profile'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()