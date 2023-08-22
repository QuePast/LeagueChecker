import re
import secrets

# Constants for SSLAdapter
CIPHERS = [
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-ECDSA-CHACHA20-POLY1305',
    'ECDHE-RSA-AES128-GCM-SHA256',
    'ECDHE-RSA-CHACHA20-POLY1305',
    'ECDHE+AES128',
    'RSA+AES128',
    'ECDHE+AES256',
    'RSA+AES256',
    'ECDHE+3DES',
    'RSA+3DES'
]

BASE_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json, text/plain, */*"
}

# User agent for requests
USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

# URLs for various endpoints
AUTH_URL = "https://auth.riotgames.com/api/v1/authorization"
USERINFO_URL = "https://auth.riotgames.com/userinfo"

# Riot client version (this can be updated or fetched dynamically if needed)
RIOTCLIENT = ''

# Pattern for extracting tokens
TOKEN_PATTERN = re.compile(r'access_token=([\w.-]+).*id_token=([\w.-]+).*expires_in=(\d*)')

# Error Codes
ERROR_NO_ACCESS_TOKEN = 6
ERROR_AUTH_FAILURE = 3
ERROR_RATE_LIMITED = 1
ERROR_MULTI_FACTOR_AUTH = 3
ERROR_CLOUDFLARE = 5

# Function to generate a random nonce of specified length
def generate_nonce(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

# Auth Data for authentication request
AUTH_DATA = {
    "acr_values": "urn:riot:bronze",
    "claims": "",
    "client_id": "riot-client",
    "nonce": generate_nonce(22),
    "redirect_uri": "http://localhost/redirect",
    "response_type": "token id_token",
    "scope": "openid link ban lol_region"
}
