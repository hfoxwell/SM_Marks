"""
    Author: Hayden Foxwell
    Date:   08/08/2024
    Purpose:
        To extract marks from SM Marks so they can be easily entered into 
        other programs for use in the Studies Department
"""

###
# Imports
###
# Global Packages
import requests

# Local imports
from src.actions import Authenticator, SMAuthenticator
# ============ #

###
# Globals
###

# ============ #

###
# MARK: Main Function
###


def main():
    """Main entry point for Application"""
     # Variables
    res: requests.Response = requests.Response()
    authenticator: Authenticator = SMAuthenticator(BASE_URL, USERNAME, PASSWORD)
    
    # Load Environment Variables
    
    # Authenticate with API
    try:
        authenticator.authenticate()
    except requests.exceptions.ConnectionError as e:
        print("Unable to connect to SM Marks, please check credentials and connection")
        raise e
    
    print(f"Authenticator: {authenticator.session_key= } {authenticator.token_key= }")


###
# Auxiliary functions
###

# ============ #

if __name__ == '__main__':
    main() # Run entry point