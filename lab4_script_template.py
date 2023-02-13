from sys import argv
import os
import re
from log_analysis import filter_log_by_regex, get_log_file_path_from_cmd_line
import pandas as pd

def main():
    log_file = get_log_file_path_from_cmd_line()

    #records = filter_log_by_regex(log_file, r'SRC=(.*?) DST = (.*?) LEN=(.*?)', ignore_case=True)

    dpt_tally = tally_port_traffic(log_file)

    for dpt, count in dpt_tally.items():
        if count > 100:
            generate_port_traffic_report(log_file, dpt)

    return



# TODO: Step 8
def tally_port_traffic(log_file):
    dest_port_logs = filter_log_by_regex(log_file, r'DPT=(.*?)')[1]

    dpt_tally = {}
    for dpt_tuple in dest_port_logs:
        dpt_tally[dpt_tuple[0]] = dpt_tally.get(dpt_tuple[0], 0) + 1


    return

# TODO: Step 9
def generate_port_traffic_report(log_file, port_number):
    
    regex = r"^(.{6}) (.{8}).*SRC=(.+?) DST =(.+?) " + f"DPT=({port_number})"

    captured_data = filter_log_by_regex(log_file, regex)[1]

    report_df = pd.DataFrame(captured_data)
    report_header = ('Date', 'Time', 'Source IP Address', 'Destination IP Address', 'Source Port', 'Destination Port')

    report_df.to_csv(f"destination_port_{port_number}_report.csv", index=False, header = report_header)
    

    return

# TODO: Step 11
def generate_invalid_user_report(log_file):
    return

# TODO: Step 12
def generate_source_ip_log(log_file, ip_address):
    return

if __name__ == '__main__':
    main()