import csv
import os
import time
import pyperclip
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CSVHandler(FileSystemEventHandler):
    def __init__(self, output_file):
        self.output_file = output_file

    def on_created(self, event):
        # Get the file name from the event
        file_name = os.path.basename(event.src_path)
        # Process only if the created file is a CSV file and starts with "subscription_details__"
        if file_name.endswith('.csv') and file_name.startswith('subscription_details__'):
            print(f"New file detected: {event.src_path}")
            self.replace_strings_in_csv(event.src_path, self.output_file)

    def replace_strings_in_csv(self, input_file, output_file):
        # Open the input CSV file for reading as a text file
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            # Open the output text file for writing
            with open(output_file, mode='w', encoding='utf-8') as outfile:
                for line in infile:
                    # Replace '","' with '|' and remove all double quotes
                    modified_line = line.replace('","', '|').replace('"', '|')
                    # Write the modified line to the output file
                    outfile.write(modified_line)
            print(f"Processed file: {input_file}")

            # Copy the modified content to the clipboard
            with open(output_file, 'r', encoding='utf-8') as f:
                clipboard_content = f.read()
                pyperclip.copy(clipboard_content)
            print("Output copied to clipboard")

def monitor_folder(folder_to_watch, output_file):
    event_handler = CSVHandler(output_file)
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    print(f"Monitoring folder: {folder_to_watch}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Usage example
download_folder = '/Users/saguirre/Downloads'  # Replace with the path to your download folder
output_file = 'CRM_formatted.txt'  # Replace with your desired output file name

monitor_folder(download_folder, output_file)
