import time
import os
import subprocess
import re

# Regular Expression for email
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Email Validating function
def get_email(data_line):
    re_compiler = re.compile(email_regex)
    finded_email = re_compiler.search(data_line)
    try:
        return finded_email.group()
    except:
        pass

def get_emails(com_name, limit=100, engine='google'):
    try:
        os.chdir('/root/Downloads/theHarvester/')
        subprocess.run(f'python3 theHarvester.py -d {com_name} -l {limit} -b {engine} | tee temp_file.txt', shell=True)
        harvest_file = open('temp_file.txt')
        lines = harvest_file.readlines()
        
        # Scanning file and getting data
        emails = list(set(map(get_email, lines)))

        while None in emails:
            emails.remove(None)

        print("\n")
        print(f"No of emails we founded are -> {len(emails)}")
        for single_email in emails:
            print(single_email)
    except Exception as e:
        print(e)

get_emails(com_name='iitk.ac.in', engine='google')