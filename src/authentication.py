import requests
from src.data import (
    RIOTCLIENT, AUTH_URL, USERINFO_URL, BASE_HEADERS, 
    TOKEN_PATTERN, ERROR_NO_ACCESS_TOKEN, ERROR_AUTH_FAILURE, 
    ERROR_RATE_LIMITED, ERROR_MULTI_FACTOR_AUTH, ERROR_CLOUDFLARE, 
    AUTH_DATA
)
from src.utils import SSLAdapter

class Account:
    def __init__(self):
        self.code = None
        self.errmsg = None
        self.token = None

class Auth:
    def __init__(self) -> None:
        self.useragent = RIOTCLIENT

    def _set_session_headers(self, session):
        headers = BASE_HEADERS.copy()
        headers['User-Agent'] = f'RiotClient/{self.useragent} (Windows;10;;Professional, x64)'
        session.headers = headers

    def _handle_response_errors(self, response):
        if "access_token" not in response.text:
            print("No access token found in the response.")
            return ERROR_NO_ACCESS_TOKEN
        if 'invalid_session_id' in response.text or "auth_failure" in response.text:
            print("Authentication failure detected.")
            return ERROR_AUTH_FAILURE
        if 'rate_limited' in response.text:
            print("Rate Limited.")
            return ERROR_RATE_LIMITED
        if 'multifactor' in response.text:
            print("Multi-factor authentication required.")
            return ERROR_MULTI_FACTOR_AUTH
        if 'cloudflare' in response.text:
            print("Rate Limited.")
            return ERROR_CLOUDFLARE
        return None

    def authenticate(self, logpass: str = None, username=None, password=None, proxy=None) -> Account:
        print(f"Starting authentication for: {logpass if logpass else username}")
        account = Account()
        session = requests.Session()
        self._set_session_headers(session)
        session.mount('https://', SSLAdapter())

        if username is None:
            username, password = logpass.split(':')

        try:
            r = session.post(AUTH_URL, json=AUTH_DATA, proxies=proxy, timeout=20)
            r.raise_for_status()
            login_data = {
                'type': 'auth',
                'username': username.strip(),
                'password': password.strip()
            }
            r2 = session.put(AUTH_URL, json=login_data, proxies=proxy, timeout=20)
            r2.raise_for_status()

            if "access_token" in r2.text:
                print("Authentication successful!")
            else:
                account.code = self._handle_response_errors(r2)
                return account

        except requests.RequestException as e:
            print(f"Request error: {e}")
            account.code = ERROR_NO_ACCESS_TOKEN
            return account

        try:
            data = r2.json()
        except ValueError:
            print("Failed to decode JSON response.")
            account.code = ERROR_NO_ACCESS_TOKEN
            return account

        uri = data.get('response', {}).get('parameters', {}).get('uri')
        if uri:
            matches = TOKEN_PATTERN.findall(uri)
            if matches:
                token, _, _ = matches[0]
                account.token = token
            else:
                account.code = self._handle_response_errors(r2)
                return account
        else:
            print("The expected structure in the data was not found.")
            return account

        return account

    def get_user_info(self, token):
        headers = {
            'User-Agent': f'RiotClient/{self.useragent}',
            'Authorization': f'Bearer {token}',
        }
        try:
            r = requests.get(USERINFO_URL, headers=headers)
            if r.status_code == 200:
                return r.json()
            else:
                print(f"Failed to retrieve user info. Status code: {r.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error while retrieving user info: {e}")
            return None