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

# Internal imports

# Abstract base class
class Authenticator(ABC):
    """ Base Class for Authentication """

    @abstractmethod
    def authenticate(self):
        """ Authenticates with the Endpoint """


# Concrete class
class SMAuthenticator(Authenticator):
    """ Represents an authentication with SM Marks"""
    # Constants
    STATUS_SUCCESS: str = "OKAY"
    REQUEST_TIMEOUT: int = 5    # in Seconds

    def __init__(self, url: str, username: str, password: str) -> None:
        super().__init__()
        # variables required to authenticate
        self.__base_url: str = url
        self.__user_name: str = username
        self.__password: str = password

        # variables
        session_key: str = ""
        token_key: str = ""

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
        except requests.exceptions.HTTPError:
            raise requests.exceptions.ConnectionError("Unable to connect to SM API", response=response)

        except requests.JSONDecodeError:
            raise requests.exceptions.ConnectionError("Unable to decode response JSON.", response=response)

        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError(
                "Unable to make valid connection to SM Marks, check username or password",
                response=response
                )

        # Extract session keys
        self.token_key, self.session_key = self.__get_session_keys(data)

    def __request_api(self):

        # declare Params
        params = {
            'apiuser': self.__user_name,
            'apipassword': self.__password
        }

        # Make the POST request
        response = requests.post(
            url=f"{self.__base_url}/authenticate.lc",
            data=params,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            timeout=self.REQUEST_TIMEOUT
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