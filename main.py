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
import csv


# Local imports
from src.actions import Authenticator, SMAuthenticator
from src.models import MarkBook, User

# ============ #

###
# Globals
###
DOT_ENV_FILE_LOC = "./.env"
CURRENT_YEAR = "2024"
YEAR_GROUP_TO_FIND = "12"
CSV_FILE = "test.csv"

# ============ #

###
# MARK: Main Function
###


def main():
    """Main entry point for Application"""
    ### Variables
    csv_writer = csv.writer(open(CSV_FILE, 'w'))
    markbook_data: list[tuple] = []
    invalid_markbooks: list[MarkBook] = []

    # Load Configuration
    config: dict[str, str] = load_config()
    
    # authenticate
    auth: Authenticator = authenticate()    
    
    # Get users
    users: list[User] = get_users(auth)
    
    
    # get markbook list
    list_requester: GetRequester = ListMarkbookRequester(auth)
    mb_list: list[MarkBook] = list_requester.get()
    mb_list = [markbook 
               for markbook in mb_list 
               if markbook.year == CURRENT_YEAR or
               CURRENT_YEAR in markbook.name
               ]
    mb_list = [markbook 
               for markbook in mb_list 
               if YEAR_GROUP_TO_FIND in markbook.course
               ]
    
    # print out some markbooks
    markbook_requester: GetRequester = MarkBookRequester(auth)
    
    print(f'{"Markbook information":#^40}')
    print(f"{len(mb_list)= }")
    print(f'{"#":=<29}')
    
    # Write out CSV Headers
    csv_writer.writerow(("Markbook", "SID", "Student Name", "Mark"))
    
    # Iterate over all the retrieved markbooks
    for book in mb_list:
        # Get a markbook from the API, Returns a list but only one
        # item is in the list, so the value is popped to unwrap the list
        # also acts as an optional unwrap. Will raise an error if no 
        # item exists
        markbook: MarkBook = markbook_requester.get(book.key).pop()
        
        # Finds the NESA task in the list of tasks in the markbook
        # This acts to return an optionally populated list which when
        # force unwrapped by pop will raise an error. 
        nesa_task = [task for task in markbook.tasks 
                    if task.name.lower() in "Final NESA Mark".lower()]
        
        # Try to get the NESA task from the markbook
        # if it does not exist, then print out failure message
        try:
            nesa_task = nesa_task.pop()
        except IndexError:
            invalid_markbooks.append(book)
            continue
        
        print(f"\n{book.name:#^30}")
        
        # Get the index of the task
        task_index = markbook.tasks.index(nesa_task)
        
        for student in markbook.students:
            # Variables
            result:str = ""
            
            # Skip out of bounds errors
            # If the task has no data, then it won't be in the student
            # task list
            if task_index > len(student.rounded_results) - 1: 
                result = "NAN"
            else:
                # Assign result to result string for printing 
                result = student.rounded_results[task_index]
            
            # Print out formatted student results
            print(
                f'{student.student_ID:<10}{student.given_name + " " +student.family_name:<30}{result:>5}'
                )
            # Write csv values
            csv_writer.writerow(
                (
                    markbook.name,
                    student.student_ID,
                    student.given_name + " " + student.family_name,
                    result
                 )
            )
    
    print(f'{"Invalid Markbook information":#^40}')
    print(f"{len(invalid_markbooks)= }")
    print(f'{"#":=<29}')
        
    for book in invalid_markbooks:
        print(f"{book.name} is not configured correctly")


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

def authenticate() -> Authenticator:
    authenticator: Authenticator = SMAuthenticator(BASE_URL, USERNAME, PASSWORD)
    
    # Authenticate with API
    try:
        authenticator.authenticate()
    except requests.exceptions.ConnectionError as e:
        print("Unable to connect to SM Marks, please check credentials and connection")
        raise e
    
    print(f"Authenticator: {authenticator.session_key= } {authenticator.token_key= }")
    
    return authenticator

def get_users(auth: Authenticator) -> list[User]:
    """Gets users from the SM Marks Program"""
    ''' Variables '''
    users: list[User] = []
    # Create 
    requester: GetRequester = UserRequester(auth)
    
    users = requester.get()
    
    return users

# ============ #

if __name__ == "__main__":
    main()  # Run entry point