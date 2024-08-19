"""
    Author: Hayden Foxwell
    Date:   08/08/24
    Purpose:
        A class for the storage of sessions:
"""

class session:
    """Represents a session with the API"""
    
    session_token = ""
    
    def __init__(self, authenticator, ) -> None:
        # Get an authenticator
        self.authenticator = authenticator