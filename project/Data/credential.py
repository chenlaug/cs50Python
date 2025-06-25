class Credential:

    def __init__(self, site:str, username:str, password:str):
        self.site = site
        self.username = username
        self.password = password

    def __str__(self) -> str:
        return f"(site={self.site}, username={self.username}, password={self.password})"

    # Methods
    def to_dict(self) -> dict:
        return {
            "site": self.site,
            "username": self.username,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["site"], data["username"], data["password"])

    # Getters for the properties
    @property
    def site(self) -> str:
        return self._site

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    # Setters for the properties
    @site.setter
    def site(self, value: str) -> None:
        self._site = value

    @username.setter
    def username(self, value: str) -> None:
        self._username = value

    @password.setter
    def password(self, value: str) -> None:
        self._password = value
