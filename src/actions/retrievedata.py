from abc import ABC, abstractmethod


class GetRequester:
    """Creates Get Requests"""

    def _get_request(
        self, url: str, action: str, session_key: str, session_token: str, params: dict
    ) -> requests.Response:
        """Sends a get request to the given URL"""
        # Variables
        response: requests.Response = requests.Response()

        # Get request to the requested URL
        response = requests.get(url=url, params=params)

        # Raise any HTTP errors which occur
        response.raise_for_status()

        # SM marks returns JSON Responses regardless of if
        # there was an error. The below code will check for
        # STATUS OKAY
        try:
            if response.json().get("status"):
                if response.json()["status"] != "OKAY":
                    raise requests.exceptions.RequestException("Invalid request")
        except requests.JSONDecodeError as e:
            print(f"Could not decode markbook response. {e}")
            raise e

        return response


class PostRequester(ABC):
    """Creates Post Requests"""

    @abstractmethod
    def _post_request(
        self, url: str, action: str, session_key: str, session_token: str
    ) -> requests.Response:
        """Sends a post request to the given URL"""


class Builder(ABC):
    """Represents building of sub object"""

    @abstractmethod
    def get(self) -> list:
        """Get the requested item from the requester"""


class MarkBookRequester(GetRequester, Builder):

    def __init__(self, auth: Authenticator) -> None:
        super().__init__()

        # Private
        # take in an authenticator for the authenticated session:
        self.__authenticator: Authenticator = auth
        self.__action = (
            "getmarkbook"  # every markbook requester has this included in request
        )

    def _get_request(
        self, url: str, action: str, session_key: str, session_token: str, params: dict
    ) -> Response:
        return super()._get_request(url, action, session_key, session_token, params)

    def get(self, key: str) -> list:
        # Variables
        markbook: MarkBook
        task_list: list[Task] = []
        student_list: list[Student] = []

        # Create params
        params = {
            "action": self.__action,
            "sessiontoken": self.__authenticator.token_key,
            "sessionkey": self.__authenticator.session_key,
            "apikey": API_KEY,
            "key": key,
        }

        # Try to get the response from SM Marks
        try:
            response = self._get_request(
                url=self.__authenticator.base_url,
                action=self.__action,
                session_key=self.__authenticator.session_key,
                session_token=self.__authenticator.token_key,
                params=params,
            )
        except Exception as e:
            print("Could not build markbook list.")
            raise e

        # Raise any errors
        response.raise_for_status()

        # parse json into a dictionary
        data = response.json()

        # Create tasks objects
        for item in data.get("tasklist"):
            task_list.append(
                Task(item["key"], item["name"], item["maximum"], item["decimalplaces"])
            )

        # Create students objects
        for item in data.get("studentlist"):
            student_list.append(
                Student(
                    item["key"],
                    item["studentid"],
                    item["familyname"],
                    item["givename"],
                    item["preferredname"],
                    item["rawresults"],
                    item["roundedresults"],
                )
            )

        markbook = MarkBook(
            data.get("markbookkey"),
            data.get("markbookname"),
            data.get("ownerkey"),
            data.get("markbookyear"),
            data.get("markbookcourse"),
            tasks=task_list,
            students=student_list,
        )

        return [markbook]


class ListMarkbookRequester(GetRequester, Builder):

    def __init__(self, auth: Authenticator) -> None:
        super().__init__()
        # Private
        self.__action = "markbooklist"
        self.__authenticator: Authenticator = auth

    def _get_request(
        self, url: str, action: str, session_key: str, session_token: str, params: dict
    ) -> Response:
        return super()._get_request(url, action, session_key, session_token, params)

    def get(self) -> list:

        # Variables
        markbook_list: list[MarkBook] = []

        # Create params
        params = {
            "action": self.__action,
            "sessiontoken": self.__authenticator.token_key,
            "sessionkey": self.__authenticator.session_key,
            "apikey": API_KEY,
        }

        try:
            response = self._get_request(
                url=self.__authenticator.base_url,
                action=self.__action,
                session_key=self.__authenticator.session_key,
                session_token=self.__authenticator.token_key,
                params=params,
            )
        except Exception as e:
            print("Could not build markbook list.")
            raise e

        # Raise any errors
        response.raise_for_status()

        data = response.json()

        for item in data.get("list"):
            markbook_list.append(
                MarkBook(
                    item["key"],
                    item["name"],
                    item["owner"],
                    item["year"],
                    item["course"],
                    [],
                    [],
                )
            )

        return markbook_list


class UserRequester(GetRequester, Builder):

    def __init__(self, auth: Authenticator) -> None:
        super().__init__()
        # Private
        self.__action = "userlist"
        self.__authenticator: Authenticator = auth

    def _get_request(
        self, url: str, action: str, session_key: str, session_token: str, params: dict
    ) -> Response:
        return super()._get_request(url, action, session_key, session_token, params)

    def get(self) -> list:
        # Variables
        user_list: list[User] = []

        # Create params
        params = {
            "action": self.__action,
            "sessiontoken": self.__authenticator.token_key,
            "sessionkey": self.__authenticator.session_key,
            "apikey": API_KEY,
        }

        try:
            response = self._get_request(
                url=self.__authenticator.base_url,
                action=self.__action,
                session_key=self.__authenticator.session_key,
                session_token=self.__authenticator.token_key,
                params=params,
            )
        except Exception as e:
            print("Could not build markbook list.")
            raise e

        # Raise any errors
        response.raise_for_status()

        data = response.json()

        for item in data.get("list"):
            user_list.append(
                User(item["key"], item["name"], item["loginid"], item["email"])
            )

        return user_list
