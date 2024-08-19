"""
    Author: Hayden Foxwell
    Date:   08/08/24
    Purpose:
        A class tracking of sessions to the API.
        
    Changelog:
        - [H Foxwell (19/08/24)] 
            Added session timeout as specified in
            SM marks documentation. Session expires every 20
            min requiring a new token and key.
"""
###
# MARK: Imports
###
# Global imports
import requests

# Local imports
from .actions.authenticate import Authenticator

# ====================== #

class Session(requests.Session):
    """Represents a session with the API"""
    
    # Constants    
    SESSION_TIMEOUT_SEC: int = (20 * 60) # Session times out in 20 min
    
    def __init__(self, authenticator: Authenticator) -> None:
        # Initialise superclass
        super().__init__()
        
        # Initalise authenticated state to false
        self.authenticated: bool = False
        
        # Get authenticator with which to authenticate
        self.authenticator = authenticator