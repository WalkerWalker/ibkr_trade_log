from dataclasses import dataclass
from typing import Optional

from urllib.parse import quote_plus

from bootstrap.ddd import ValueObject


@dataclass(frozen=True)
class RdbConfig(ValueObject):
    autocommit = True
    autoflush = True
    scheme = "postgresql"

    url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    database: Optional[str] = None

    def build_url(self):
        if self.url:
            return self.url
        else:
            return build_database_url(
                host=self.host,
                scheme=self.scheme,
                port=self.port,
                username=self.username,
                password=self.password,
                database=self.database,
            )


def build_database_url(
    host: str,
    scheme="postgresql",
    port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    database: Optional[str] = None,
):
    url_username_password = ""
    if username:
        username = quote_plus(username)
        url_username_password = f"{username}@"

        if password:
            password = quote_plus(password)
            url_username_password = f"{username}:{password}@"

    url_port = ""
    if port:
        url_port = f":{port}"

    url_database = ""
    if database:
        url_database = f"/{database}"

    return f"{scheme}://{url_username_password}{host}{url_port}{url_database}"
