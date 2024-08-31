"""
    Author:     Hayden Foxwell
    Date:       16/08/2024
    Purpose:
        This file contains the authorisation routines
        to authorise with the server, and to then to
        verify that the authorisation is valid.
"""

# external imports
from abc import ABC, abstractmethod
import requests


class Authenticator(ABC):

    # Constants
    STATUS_SUCCESS: str = "OKAY"

    def __init__(self) -> None:
        super().__init__()
        self.base_url: str
        self.session_key: str
        self.token_key: str

    @abstractmethod
    def authenticate(self):
        """Authenticates with the Endpoint"""


class SMAuthenticator(Authenticator):

    def __init__(self, url: str, username: str, password: str) -> None:
        super().__init__()
        # variables required to authenticate
        self.base_url: str = url
        self.__user_name: str = username
        self.__password: str = password

        # variables
        self.session_key: str = ""
        self.token_key: str = ""

    def authenticate(self):

        # Variables
        data: dict = {}

        # Make request
        try:
            response: requests.Response = self.__request_api()

            # Try to decode data
            data = response.json()

            # Confirm request
            self.__authentication_valid(data)

        # Exception pathway
        except requests.exceptions.HTTPError as httperr:
            raise requests.exceptions.ConnectionError(
                "Unable to connect to SM API", response=response
            )

        except requests.JSONDecodeError as jde:
            raise requests.exceptions.ConnectionError(
                "Unable to decode response JSON.", response=response
            )

        except requests.exceptions.ConnectionError as ce:
            raise requests.exceptions.ConnectionError(
                "Unable to make valid connection to SM Marks, check username or password",
                response=response,
            )

        # Extract session keys
        self.token_key, self.session_key = self.__get_session_keys(data)

    def __request_api(self):

        # declare Params
        params = {"apiuser": self.__user_name, "apipassword": self.__password}

        # Make the POST request
        response = requests.post(
            url=f"{self.base_url}/authenticate.lc",
            data=params,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        # Raises error if HTTP error occurred
        response.raise_for_status()

        return response

    def __authentication_valid(self, data: dict):
        # Constants
        STATUS_KEY = "status"

        # Variables
        valid: bool = False

        # Check return status
        if data.get(STATUS_KEY):

            valid = data[STATUS_KEY] == self.STATUS_SUCCESS

        else:
            raise requests.exceptions.InvalidJSONError("Malformed Response.")

        if not valid:
            raise requests.exceptions.ConnectionError()

    def __get_session_keys(self, data: dict) -> tuple[str, str]:
        # Constants
        SESSION_KEY = "sessionkey"
        SESSION_TOKEN = "sessiontoken"

        # Variables
        session_token: str = ""
        session_key: str = ""

        if data.get(SESSION_TOKEN) and data.get(SESSION_KEY):
            session_token = data[SESSION_TOKEN]
            session_key = data[SESSION_KEY]

        else:
            raise requests.exceptions.InvalidJSONError(
                "Missing Session token or Session key!"
            )

        return (session_token, session_key)
