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
from dotenv import dotenv_values
import requests


# Local imports
from src.actions import Authenticator, SMAuthenticator

# ============ #

###
# Globals
###
DOT_ENV_FILE_LOC = "./.env"

# ============ #

###
# MARK: Main Function
###


def main():
    """Main entry point for Application"""

    # Load Configuration
    config: dict[str, str] = load_config()

    # Variables
    authenticator: Authenticator = SMAuthenticator(
        config["BASE_URL"], config["USERNAME"], config["PASSWORD"]
    )

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
def load_config() -> dict[str, str]:
    """Loads the configuration values from the .env file in the parent
    directory.

    Raises:
        ValueError: If an invalid value is present, either None or ""

    Returns:
        dict[str, str]: Returns the configuration items and values.
    """
    # Variables
    config: dict[str, str] = {}

    config = dotenv_values(DOT_ENV_FILE_LOC)

    for key, item in config.items():
        if item is None or item == "":
            raise ValueError(
                f"Invalid Environment Configuration. Missing value for: {key}"
            )

    return config


# ============ #

if __name__ == "__main__":
    main()  # Run entry point
