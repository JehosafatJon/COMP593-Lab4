from sys import argv
import os
import re

def main():

    pass

# TODO: Step 3
def get_log_file_path_from_cmd_line():
    """Gets a filepath of a log file from the command line parameters.

    Returns:
        str: The path of the log file
    """    
    if len(argv) < 2:
        print("ERROR. Please provide a file path for a log file.")
        exit(1)
    elif not os.path.isfile(argv[1]):
        print("ERROR. Invalid file path.")
        exit(1)
    else:
        return os.path.abspath(argv[1])

# TODO: Steps 4-7
def filter_log_by_regex(log_file, regex, ignore_case=True, print_summary=False, print_records=False):
    """Gets a list of records in a log file that match a specified regex.

    Args:
        log_file (str): Path of the log file
        regex (str): Regex filter
        ignore_case (bool, optional): Enable case insensitive regex matching. Defaults to True.
        print_summary (bool, optional): Enable printing summary of results. Defaults to False.
        print_records (bool, optional): Enable printing all records that match the regex. Defaults to False.

    Returns:
        (list, list): List of records that match regex, List of tuples of captured data
    """

    list_of_matches = []
    captured_data = []

    with open(log_file, 'r') as log_file_data:
        for line in log_file_data:
            if ignore_case:
                match = re.search(regex, line, flags=re.IGNORECASE)
            else:
                match = re.search(regex, line)
            
            if match:
                list_of_matches.append(line)
                if match.lastindex:
                    captured_data.append(match.groups())

            
        if print_summary:
            print(*list_of_matches)
            
        if print_records:
            print(f"There are {len(list_of_matches)} matching records. Case {'in' if ignore_case else ''}sensitive.")


    return list_of_matches, captured_data

if __name__ == "__name__":
    main()