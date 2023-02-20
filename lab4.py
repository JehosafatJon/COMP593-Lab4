from log_analysis import filter_log_by_regex, get_log_file_path_from_cmd_line
import pandas as pd
import re

def main():
    
    # Gets path of the log file
    log_file = get_log_file_path_from_cmd_line()


    # Step 10
    dpt_tally = tally_port_traffic(log_file)
    for dpt, count in dpt_tally.items():
        if count > 100:
            generate_port_traffic_report(log_file, dpt)
            

    # Step 11 Call
    generate_invalid_user_report(log_file)

    
    # Step 12 Call
    generate_source_ip_log(log_file, '220.195.35.40')
    
    pass

# Step 8
def tally_port_traffic(log_file):
    """Creates a tally of number of times a port was searched.

    Args:
        log_file (str): Path of the log file
        
    Returns:
        (dict): Tallied totals for unique ports in the log file
    """

    dest_port_logs = filter_log_by_regex(log_file, r' DPT=(.*?) ')[1]

    dpt_tally = {}
    for dpt_tuple in dest_port_logs:
        dpt_tally[dpt_tuple[0]] = dpt_tally.get(dpt_tuple[0], 0) + 1

    return dpt_tally

# Step 9
def generate_port_traffic_report(log_file, port_number):
    """ Writes data from the records of the specified port to a csv file

    Args:
        log_file (str): Path of the log file
        port_number (str): The port number to generate the report on

    """

    regex = r'^(.{6}) (.{8}) .*SRC=(.+?) DST=(.+?) .*SPT=(.+?) ' + f'DPT=({port_number})'

    captured_data = filter_log_by_regex(log_file, regex)[1]
    report_df = pd.DataFrame(captured_data)
    
    report_header = ('Date', 'Time', 'Source IP Address', 'Destination IP Address', 'Source Port', 'Destination Port')
    report_df.to_csv(f"destination_port_{port_number}_report.csv", index=False, header=report_header)
    
    return

# Step 11
def generate_invalid_user_report(log_file):
    """ Writes a report of invalid user records to a csv file.

    Args:
        log_file (str): Path of the log file
    """

    regex = r'^(.{6}) (.{8}).*Invalid user (.*) from (.*)'

    captured_data = filter_log_by_regex(log_file, regex)[1]
    report_df = pd.DataFrame(captured_data)
    
    report_header = ('Date', 'Time', 'Username', 'IP Address')
    report_df.to_csv("invalid_users.csv", index=False, header=report_header)
    return

# Step 12
def generate_source_ip_log(log_file, ip_address):
    """ Writes the records from a specified source ip to a log file.

    Args:
        log_file (str): Path of the log file
        ip_address (str): The IP address to filter and generate the log for
    """
    
    regex = f'(.*SRC={ip_address}.*)'
    underscored_ip_address = re.sub(r"\.", "_", ip_address)

    ip_records = filter_log_by_regex(log_file, regex)[1]
    report_df = pd.DataFrame(ip_records)
    report_df.to_csv(f"source_ip_{underscored_ip_address}.log",  index=False, header=None)
    return

if __name__ == '__main__':
    main()