# app/utils/auth.py
import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)

def generate_api_token():
    return secrets.token_urlsafe(64)
