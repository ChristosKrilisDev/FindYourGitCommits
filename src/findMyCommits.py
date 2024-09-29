# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 20:47:48 2024

@author: Krilis Christos
"""

import json
from datetime import datetime, timedelta
import pandas as pd
import os


def process_commit(commit, time_threshold, is_late, type_label):
    commit_date = datetime.strptime(commit['date'], "%a %b %d %H:%M:%S %Y %z")
    commit_time = commit_date.time()  # Extract commit time

    commit_time_dt = datetime.combine(datetime.today(), commit_time)
    threshold_time_dt = datetime.combine(datetime.today(), time_threshold)

    if is_late:
        time_diff = commit_time_dt - threshold_time_dt
    else:
        time_diff = threshold_time_dt - commit_time_dt

    # Update global variables
    global count_after_hours_commits, extra_estimated_time
    count_after_hours_commits += 1
    extra_estimated_time += time_diff

    # Store commit details with type and commit time
    commit_details.append({
        'Date': commit_date.replace(tzinfo=None),  # Make timezone naive
        'Commit Time': commit_time,  # Include commit time
        'Estimated Extra Hours': str(time_diff),
        'Message': commit['message'],
        'Type': type_label  # Indicate whether this is a late or early commit
    })

    # Print commit information
    print(type_label)
    print(f"Date: {commit_date}")
    print(f"Commit Time: {commit_time}")
    print(f"Diff: {time_diff}")
    print(f"Message: {commit['message']}")
    print('-' * 40)

def export_to_excel(export_data_to_excel):
    # Create DataFrame and export to Excel
    if export_data_to_excel:
        os.makedirs(export_directory, exist_ok=True)
        df = pd.DataFrame(commit_details)
        output_filename = os.path.join(export_directory, 'commit_details.xlsx')
        df.to_excel(output_filename, index=False)
        print(f"Data exported to {output_filename} successfully.")


commits_data_path = '../data/commits.json'
export_directory = '../exportedData/'
export_data_to_excel = False

# Define time thresholds, commits between 09:00 and 17:00 will be excluded!
time_threshold_start = datetime.strptime("09:00:00", "%H:%M:%S").time()
time_threshold_end = datetime.strptime("17:00:00", "%H:%M:%S").time()
count_after_hours_commits = 0
extra_estimated_time = timedelta()
commit_details = []  # To hold details for Excel export

# Load commits from commits.json
with open(commits_data_path, 'r', encoding='utf-8') as file:
    commits = json.load(file)

for commit in commits:
    commit_date = datetime.strptime(commit['date'], "%a %b %d %H:%M:%S %Y %z")
    commit_time = commit_date.time()  # Extract commit time

    if commit_time > time_threshold_end:
        process_commit(commit, time_threshold_end, True, "Late")
    elif commit_time < time_threshold_start:
        process_commit(commit, time_threshold_start, False, "Early")


# Prepare total hours and minutes
total_hours = extra_estimated_time.total_seconds() // 3600
total_minutes = (extra_estimated_time.total_seconds() % 3600) // 60


print(f"\nTotal commits: {count_after_hours_commits} made after {time_threshold_end}.")
print(f"Total Extra Time: {int(total_hours)} hours and {int(total_minutes)} minutes")

export_to_excel(export_data_to_excel)


