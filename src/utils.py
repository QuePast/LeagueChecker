from src.data import CIPHERS
from requests.adapters import HTTPAdapter
from typing import Any
import ssl

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.set_ciphers(':'.join(CIPHERS))
        kwargs['ssl_context'] = context
        super().init_poolmanager(*args, **kwargs)